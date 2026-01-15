#standardized metadata to ensure retrieval and citations were consistent

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class ChunkMetadata:
    chapter_index: int
    chapter_title: str
    chapter_number_raw: Optional[str]

    subchapter: Optional[str]
    topic: Optional[str]
    subtopic: Optional[str]
    section: Optional[str]

    content_type: str          # text | table | rules | example
    table_purpose: Optional[str]

    page_number: int
    extra: Dict[str, Any]
