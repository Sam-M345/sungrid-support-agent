"""Load SunGrid markdown docs and split into chunks with section metadata."""

from __future__ import annotations

import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings

HEADER = re.compile(r"^(#{2,3})\s+(\d+(?:\.\d+)?)\s+(.+)$", re.MULTILINE)
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def _source_label(path: Path) -> str:
    """Human-readable source name for citations."""
    names = {
        "warranty_policy.md": "Warranty Policy",
        "installation_troubleshooting_guide.md": "Troubleshooting Guide",
        "safety_escalation_policy.md": "Safety Escalation Policy",
        "customer_support_sop.md": "Customer Support SOP",
        "financing_faq.md": "Financing FAQ",
    }
    return names.get(path.name, path.stem.replace("_", " ").title())


def _split_file(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8")
    source = _source_label(path)
    file_name = path.name
    documents: list[Document] = []

    matches = list(HEADER.finditer(text))
    if not matches:
        for chunk in SPLITTER.split_text(text):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source,
                        "file_name": file_name,
                        "section_id": "0.0",
                        "section_title": "Document",
                    },
                )
            )
        return documents

    for index, match in enumerate(matches):
        section_id = match.group(2)
        section_title = match.group(3).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section_body = text[start:end].strip()
        if not section_body:
            continue

        header_prefix = "#" * len(match.group(1))
        header_line = f"{header_prefix} {section_id} {section_title}"
        chunks = SPLITTER.split_text(section_body)

        for chunk_index, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=f"{header_line}\n\n{chunk}",
                    metadata={
                        "source": source,
                        "file_name": file_name,
                        "section_id": section_id,
                        "section_title": section_title,
                        "chunk_index": chunk_index,
                    },
                )
            )

    return documents


def load_documents(docs_dir: Path | None = None) -> list[Document]:
    """Load and chunk all markdown files from the docs directory."""
    directory = docs_dir or settings.docs_dir
    paths = sorted(directory.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"No markdown files found in {directory}")

    documents: list[Document] = []
    for path in paths:
        documents.extend(_split_file(path))
    return documents
