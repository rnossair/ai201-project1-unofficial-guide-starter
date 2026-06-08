"""
Milestone 3: Document ingestion, cleaning, and chunking.

Loads all 10 sources from planning.md, cleans the text, and produces
overlapping word-based chunks (chunk_size=250, overlap=50).
Saves chunks to documents/chunks.json for the embedding stage.

Source 5 (Grinnell Student Handbook) is expected as a local PDF at:
    documents/grinnell_self_governance.pdf
Drop any saved PDF there before running; the script skips it gracefully if absent.
"""

import re
import json
import time
from pathlib import Path

import pdfplumber
import requests
from bs4 import BeautifulSoup

CHUNK_SIZE = 250  # words
OVERLAP = 50      # words

SOURCES = [
    {
        "id": 1,
        "url": "https://old.reddit.com/r/Grinnell/comments/n4po1g/what_are_the_different_dorm_buildings_on_campus/",
        "type": "reddit",
        "description": "r/Grinnell: What are the different dorm buildings on campus?",
    },
    {
        "id": 2,
        "url": "https://www.grinnell.edu/news/self-gov-101",
        "type": "web",
        "description": "Grinnell Website: Self Gov 101",
    },
    {
        "id": 3,
        "url": "https://www.grinnell.edu/news/self-defining-self-governance",
        "type": "web",
        "description": "Grinnell Website: Self-Defining Self-Governance",
    },
    {
        "id": 4,
        "url": "https://thesandb.com/39417/article/self-gov-is-dead-did-it-ever-exist-anyway/",
        "type": "sandb",
        "description": "Scarlet & Black: Self-Gov Is Dead — Did It Ever Exist Anyway?",
    },
    {
        "id": 5,
        "path": "documents/grinnell_self_governance.pdf",
        "type": "pdf",
        "description": "Grinnell Student Handbook: Self-Governance at Grinnell College",
    },
    {
        "id": 6,
        "url": "https://www.grinnell.edu/campus-life/student-life/living-spaces/residence-halls",
        "type": "web",
        "description": "Grinnell Website: Residence Halls",
    },
    {
        "id": 7,
        "url": "https://old.reddit.com/r/Grinnell/comments/xgbnuo/hows_the_social_life/",
        "type": "reddit",
        "description": "r/Grinnell: How's the social life?",
    },
    {
        "id": 8,
        "url": "https://www.grinnell.edu/life/organizations",
        "type": "web",
        "description": "Grinnell Website: Student Organizations",
    },
    {
        "id": 9,
        "url": "https://thesandb.com/38899/article/nightlife-in-the-prairie/",
        "type": "sandb",
        "description": "Scarlet & Black: Nightlife in the Prairie",
    },
    {
        "id": 10,
        "url": "https://thesandb.com/46692/article/student-speaks-dorm-hall-defense/",
        "type": "sandb",
        "description": "Scarlet & Black: Student Speaks — Dorm Hall Defense",
    },
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ai201-project/1.0; "
        "educational research bot; contact: nossairr@grinnell.edu)"
    )
}


def fetch_reddit(url: str) -> str:
    """Scrape post (siteTable) + comments (commentarea) from old.reddit.com."""
    resp = requests.get(url, headers=_HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    texts: list[str] = []

    site_table = soup.find(id="siteTable")
    if site_table:
        md = site_table.find("div", class_="md")
        if md:
            texts.append(md.get_text(separator=" ", strip=True))

    comment_area = soup.find(class_="commentarea")
    if comment_area:
        for comment in comment_area.find_all("div", class_="comment"):
            md = comment.find("div", class_="md")
            if md:
                body = md.get_text(separator=" ", strip=True)
                if body:
                    texts.append(body)

    return "\n\n".join(texts)


def fetch_sandb(url: str) -> str:
    """Extract article body from Scarlet & Black using #sno-story-body-content."""
    resp = requests.get(url, headers=_HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    body = soup.find(id="sno-story-body-content")
    if not body:
        return ""
    for tag in body(["script", "style"]):
        tag.decompose()
    return body.get_text(separator=" ", strip=True)


def fetch_web(url: str) -> str:
    resp = requests.get(url, headers=_HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()

    main = (
        soup.find("article")
        or soup.find("main")
        or soup.find(class_=re.compile(r"(content|entry|post|article)", re.I))
        or soup.body
    )
    return main.get_text(separator=" ", strip=True) if main else ""


def fetch_pdf(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    pages: list[str] = []
    with pdfplumber.open(p) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # markdown links → label
    text = re.sub(r"[^\S\n]+", " ", text)                  # collapse inline whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)                 # collapse excess blank lines
    text = re.sub(r"[^\x00-\x7F]+", " ", text)            # strip non-ASCII
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap
    return chunks


def load_source(source: dict) -> list[dict]:
    src_type = source["type"]
    label = source["description"]
    src_id = source["id"]
    print(f"  [{src_id}] {label}")

    try:
        if src_type == "reddit":
            raw = fetch_reddit(source["url"])
            location = source["url"]
        elif src_type == "sandb":
            raw = fetch_sandb(source["url"])
            location = source["url"]
        elif src_type == "pdf":
            raw = fetch_pdf(source["path"])
            location = source["path"]
        else:
            raw = fetch_web(source["url"])
            location = source["url"]
    except FileNotFoundError as exc:
        print(f"       SKIP: {exc}")
        return []
    except Exception as exc:
        print(f"       WARNING: failed to fetch ({exc})")
        return []

    cleaned = clean_text(raw)
    if not cleaned:
        print("       WARNING: no text extracted")
        return []

    chunks = chunk_text(cleaned)
    print(f"       {len(cleaned.split())} words -> {len(chunks)} chunks")

    return [
        {
            "chunk_id": f"src{src_id}_chunk{i}",
            "source_id": src_id,
            "source_url": location,
            "source_description": label,
            "text": chunk,
        }
        for i, chunk in enumerate(chunks)
    ]


def main() -> None:
    out_dir = Path("documents")
    out_dir.mkdir(exist_ok=True)

    all_chunks: list[dict] = []

    for source in SOURCES:
        chunks = load_source(source)
        all_chunks.extend(chunks)
        if source.get("type") in ("web", "reddit"):
            time.sleep(1)  # polite crawl delay

    out_path = out_dir / "chunks.json"
    out_path.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone. {len(all_chunks)} total chunks saved to {out_path}")
    print(f"Chunk size: {CHUNK_SIZE} words | Overlap: {OVERLAP} words")


if __name__ == "__main__":
    main()
    

