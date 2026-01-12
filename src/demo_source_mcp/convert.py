from urllib.parse import urljoin

from fastmcp.exceptions import ToolError
from markdownify import markdownify

from demo_source_mcp.base import ContentType, Page
from demo_source_mcp.igloo import Igloo


def convert_to_page(object_data: dict, igloo: Igloo):
    """Covert raw igloo object data into a Page object."""
    extension = object_data.get("fileExtension", ".html")
    if extension != ".html":
        content = igloo.get_document_binary(object_data["id"])
        content_type = ContentType.FILE
    else:
        content_str: str = object_data["content"]
        content = content_str.encode("utf-8")
        content_type = ContentType.PAGE
    if not content:
        # It may be a widget, so try pulling any available HTML content from the widget
        html_widget_content = igloo.get_ig_widget_html_content_by_path(object_data["href"])
        content = html_widget_content if html_widget_content else content
    page = Page(
        name=object_data["title"],
        content=content,
        content_type=content_type,
        url=urljoin(igloo.endpoint, object_data["href"]),
        page_id=object_data["id"],
        title=object_data["title"],
        url_path=object_data["href"],
        is_published=object_data["isPublished"],
        is_archived=object_data["IsArchived"],
        is_scheduled_for_archiving=object_data["IsScheduledForArchiving"],
        statistics=object_data["statistics"],
        created=object_data.get("created", {}),
        modified=object_data.get("modified", {}),
        published=object_data.get("published", {}),
        extension=extension,
    )
    return page


def convert_to_markdown(page: Page) -> str:
    """Change page content from HTML to markdown."""
    if page.extension == ".html":
        return markdownify(page.content)
    raise ToolError(f"Cannot convert page to Markdown: Unsupported extension {page.extension}")
