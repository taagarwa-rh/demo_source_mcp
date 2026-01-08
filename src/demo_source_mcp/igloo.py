import logging
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

import demo_source_mcp.pyigloo as pyigloo

load_dotenv()

logger = logging.getLogger(__name__)


class Igloo:
    """Class for connecting to igloo."""

    def __init__(self):
        """Initialize."""
        self.endpoint: str = os.environ.get("IGLOO_ENDPOINT", None)
        self.api_user: str = os.environ.get("IGLOO_USER", None)
        self.api_pass: str = os.environ.get("IGLOO_PASS", None)
        self.api_key: str = os.environ.get("IGLOO_API_KEY", None)
        self.access_key: str = os.environ.get("IGLOO_ACCESS_KEY", None)
        self.community_key: str = os.environ.get("IGLOO_COMMUNITY_KEY", None)

        info = {
            "ACCESS_KEY": self.access_key,
            "API_KEY": self.api_key,
            "API_USER": self.api_user,
            "API_PASSWORD": self.api_pass,
            "API_ENDPOINT": self.endpoint,
        }
        self.session = pyigloo.igloo(info=info, communitykey=self.community_key)

    def get_object(self, object_id: str) -> dict:
        """Get a single object."""
        response = self.session.objects_view(objectid=object_id)
        return response

    def get_object_bypath(self, path: str) -> dict:
        """Get an object by its path."""
        response = self.session.objects_bypath(path=path)
        return response

    def get_id_from_path(self, path: str) -> str:
        """Get the id of a object by its path."""
        response = self.get_object_bypath(path=path)
        if response is None:
            raise ValueError(f"Path {path} does not exist. Please check the path and try again.")
        object_id: str = response["id"]
        return object_id

    def get_ig_widget_html_content_by_path(self, path: str) -> bytes:
        """Get the HTML content of a widget object."""
        # TODO: This could use some work
        response = self.session.get_web_uri(path)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, features="html.parser")

        # classes = ["ig-widget-type-call-to-action", "ig-widget-type-wiki", "ig-widget-type-html", "ig-widget-type-group"]
        html_contents = soup.find_all("div", {"class": "ig-cpt"})

        html_content = "\n".join([str(c) for c in html_contents])
        html_bytes = html_content.encode("utf-8")
        return html_bytes

    def get_children_from_parent(self, parent_path: str = None, parent_object_id: str = None, recursive: bool = False):
        """Get all children from a parent url path."""
        # Get the parent object id
        if parent_path is None and parent_object_id is None:
            raise ValueError("Must set one of 'parent_path' or 'parent_object_id'")
        if parent_path is not None:
            logger.info(f"Fetching objects under path {parent_path}")
            parent_object_id = self.get_id_from_path(path=parent_path)

        # Get all the children
        all_children = []
        for child in self.session.get_all_children_from_object(parent_object_id, pagesize=100):
            children = [child]
            if recursive:
                try:
                    child_object_id = child["id"]
                    childs_children = self.get_children_from_parent(parent_object_id=child_object_id, recursive=True)
                except TypeError:
                    continue
                children.extend(childs_children)
            all_children.extend(children)

        return all_children

    def get_document_binary(self, document_id: str) -> bytes:
        """Get the contents of a document."""
        # Send a request to the /documents/document_id/view_binary endpoint to get file contents
        endpoint = self.session.endpoint
        api_root = self.session.IGLOO_API_ROOT_V1
        url = "{0}{1}/documents/{2}/view_binary".format(endpoint, api_root, document_id)
        headers = {b"Accept": "application/json"}
        response = self.session.igloo.get(url=url, headers=headers)
        return response.content

    def get_attachments(self, object_id: str):
        """Get all attachments on an object."""
        # Get page metadata
        page = self.get_object(object_id=object_id)
        # List the attachments
        page_attachments = self.session.attachments_view(objectid=object_id)
        items = page_attachments.get("items", [])
        # Get information about each attachment
        attachments = []
        for item in items:
            document_id = item["ToId"]
            document_metadata = self.session.objects_view(document_id)
            document_binary = self.get_document_binary(document_id=document_id)
            attachment = document_metadata | {"contentBinary": document_binary, "attachedToHref": page["href"]}
            attachments.append(attachment)
        return attachments

    def get_image(self, image_href: str) -> bytes:
        """Get an image from a given href."""
        endpoint = self.session.endpoint
        url = "{0}{1}".format(endpoint, image_href)
        headers = {b"Accept": "application/json"}
        response = self.session.igloo.get(url=url, headers=headers)
        return response.content

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search for content based on a query. Returns a list of dictionaries containing the search results."""
        raw_search_result: dict = self.session.search_contentdetailed(query=query, limit=limit)
        search_results: list[dict] = raw_search_result.get("results", [])
        return search_results
