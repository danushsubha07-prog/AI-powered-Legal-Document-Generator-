from __future__ import annotations

import html
import re


def sanitize_text(text: str) -> str:
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def terms_to_list(terms: str) -> list[str]:
    return [item.strip() for item in terms.split(";") if item.strip()]


def text_to_html(text: str) -> str:
    escaped = html.escape(sanitize_text(text))
    escaped = re.sub(r"(?m)^([A-Z][A-Z0-9 &/()'-]{2,})$", r"<h3>\1</h3>", escaped)
    escaped = escaped.replace("\n\n", "</p><p>").replace("\n", "<br>")
    return f"<p>{escaped}</p>"


def safe_filename(document_type: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", document_type).strip("_").lower()
    return slug or "legal_document"
