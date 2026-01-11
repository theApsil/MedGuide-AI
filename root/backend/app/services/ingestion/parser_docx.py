from pathlib import Path
from docx import Document


def parse_docx(path: str | Path) -> dict:
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return {
        "text": text,
        "sections": [],
        "metadata": {
            "source": "docx",
            "filename": Path(path).name,
        },
    }
