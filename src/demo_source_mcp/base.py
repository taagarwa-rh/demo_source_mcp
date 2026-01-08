from enum import Enum
from typing import Optional

from pydantic import BaseModel, computed_field


class ContentType(Enum):
    """Denote the type of content in a source object."""

    ATTACHMENT = "attachment"
    FILE = "file"
    IMAGE = "image"
    PAGE = "page"


class SourceObject(BaseModel):
    """Source object data."""

    name: str
    content: bytes
    content_type: ContentType


class Attachment(SourceObject):
    """Page attachment."""

    content_type: ContentType = ContentType.ATTACHMENT


class Image(SourceObject):
    """Page embedded image."""

    mimetype: Optional[str] = None
    content_type: ContentType = ContentType.IMAGE


class Page(SourceObject):
    """Source page data."""

    url: str
    page_id: str
    title: str
    url_path: str
    extension: str
    is_published: bool
    is_archived: bool
    is_scheduled_for_archiving: bool
    statistics: dict = {}
    created: dict = {}
    modified: dict = {}
    published: dict = {}
    images: list[Image] = []
    attachments: list[Attachment] = []
    content_type: ContentType

    @computed_field
    @property
    def num_images(self) -> int:
        """Number of images."""
        return len(self.images)

    @computed_field
    @property
    def num_attachments(self) -> int:
        """Number of attachments."""
        return len(self.attachments)


class SearchResult(BaseModel):
    """Search result data."""

    id: str
    title: str
    url: str
    description: str = None
    keywords: dict = {}
    last_updated: str = None
