import logging
from urllib.parse import urljoin

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from demo_source_mcp.base import SearchResult
from demo_source_mcp.convert import convert_to_markdown, convert_to_page
from demo_source_mcp.igloo import Igloo

logger = logging.getLogger(__name__)

mcp = FastMCP("demo_source_mcp")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    """Check health of the server."""
    return PlainTextResponse("OK")


@mcp.tool
def search(query: str, limit: int = 5) -> list[SearchResult]:
    """
    Search "The Source" for pages relevant to the query.

    This will return a list of search results, each containing at minimum the id, url, and title of the content.
    Other fields that may be returned include the description and keywords in the page.

    Args:
        query (str): The query to search for.
        limit (int): The maximum number of results to return.

    Returns:
        list[SearchResult]: A list of search results. Each result contains the id, url, and title of the content. Other fields may be returned.

    """
    igloo = Igloo()
    raw_results = igloo.search(query=query, limit=limit)
    search_results = []
    for raw_result in raw_results:
        search_result = SearchResult(
            id=raw_result.get("id"),
            url=urljoin(igloo.endpoint, raw_result.get("href")),
            title=raw_result.get("title"),
            description=raw_result.get("description"),
            keywords=raw_result.get("keywords"),
            last_updated=raw_result.get("modifiedDate"),
        )
        search_results.append(search_result)
    return search_results


@mcp.tool
def get_content(id: str = None, href: str = None) -> str:
    """
    Fetch the content of a given page from "The Source" in an easy-to-understand Markdown format.

    Only one of id or href should be defined. If both are defined, the id will be used.
    If neither is defined, an error will be raised.

    Args:
        id (str, optional): Page ID. Found in search results. Defaults to None.
        href (_type_, optional):
            Page href (url). Found in the content of other pages.
            For example, in "[Finance Department](/departments/finance)", "/departments/finance" is an href.
            Defaults to None.

    Raises:
        ValueError: If neither 'id' nor 'href' is provided.

    Returns:
        str: Content of the page in markdown format.

    """
    igloo = Igloo()
    if id is not None:
        object_data = igloo.get_object(object_id=id)
    elif href is not None:
        object_data = igloo.get_object_bypath(path=href)
    else:
        raise ValueError("Either 'id' or 'href' must be provided.")
    page = convert_to_page(object_data=object_data, igloo=igloo)
    page = convert_to_markdown(page)
    return page


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    mcp.run(transport="http", host="0.0.0.0", port=8000)
