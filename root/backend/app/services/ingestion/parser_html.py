from pathlib import Path
from bs4 import BeautifulSoup


def parse_html(path: str | Path) -> dict:
    html = Path(path).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(separator="\n", strip=True)

    return {
        "text": text,
        "sections": [],
        "metadata": {
            "source": "html",
            "filename": Path(path).name,
        },
    }
