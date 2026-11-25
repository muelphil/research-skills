"""Import public OpenReview API v2 reviews or a rendered forum HTML snapshot."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import urlopen, url2pathname


class ForumHTML(HTMLParser):
    """Read review headings and field labels, independently of layout classes."""
    def __init__(self):
        super().__init__()
        self.reviews = []
        self.review = None
        self.capture = self.field = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if tag == "h4" or "note-content-field" in classes:
            self.capture = tag
            self.parts = []
            self.field = None
        elif "note-content-value" in classes and self.review and self.field:
            self.capture = "value"
            self.depth = 1
            self.parts = []
            self.lists = []
        elif self.capture == "value":
            if tag == "div":
                self.depth += 1
            if tag in ("ul", "ol"):
                start = dict(attrs).get("start") or "1"
                number = None
                if tag == "ol":
                    number = int(start) if re.fullmatch(r"\d+", start) else 1
                self.lists.append(number)
                if len(self.lists) == 1:
                    self.parts.append("\n\n")
            elif tag == "li" and self.lists:
                number = self.lists[-1]
                marker = "-" if number is None else f"{number}."
                indent = " " * (4 * (len(self.lists) - 1))
                self.parts.append(f"\n{indent}{marker} ")
                if number is not None:
                    self.lists[-1] += 1
            elif tag == "p" and self.lists:
                if not re.fullmatch(r"\n *(-|\d+\.) ", self.parts[-1]):
                    self.parts.append("\n\n" + " " * (4 * len(self.lists)))
            elif tag in ("br", "p", "tr"):
                self.parts.append("\n")
            if tag == "a" and dict(attrs).get("href"):
                self.parts.append("(" + dict(attrs)["href"] + ") ")

    def handle_data(self, data):
        if self.capture == "value" and self.lists and not data.strip() and "\n" in data:
            return
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if self.capture == "value" and tag in ("ul", "ol") and self.lists:
            self.lists.pop()
            if not self.lists:
                self.parts.append("\n\n")
        elif self.capture == "value" and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.review["fields"][self.field] = "".join(self.parts).strip()
                self.capture = self.field = None
        elif self.capture == tag:
            value = "".join(self.parts).strip()
            if tag == "h4":
                self.review = None
                if re.search(r"\bofficial review\b", value, re.I):
                    self.review = {"title": value, "fields": {}}
                    self.reviews.append(self.review)
            else:
                self.field = value.rstrip(":")
            self.capture = None


def public_reviews(source):
    url = urlsplit(source)
    if url.hostname not in ("openreview.net", "www.openreview.net") or not parse_qs(url.query).get("id"):
        raise ValueError("Expected an OpenReview forum URL with ?id=...")
    forum = parse_qs(url.query)["id"][0]
    reviews = []
    offset = 0
    while True:
        query = urlencode(dict(forum=forum, limit=100, offset=offset))
        with urlopen("https://api2.openreview.net/notes?" + query, timeout=30) as response:
            notes = json.load(response)["notes"]
        for note in notes:
            if not any(i.split("/")[-1].lower() == "official_review" for i in note.get("invitations", [])):
                continue
            reviews.append(dict(title="Official Review by " + ", ".join(note["signatures"]),
                                fields={k.replace("_", " "): v["value"] for k, v in note["content"].items()}))
        offset += len(notes)
        if len(notes) < 100:
            return reviews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    source = parser.parse_args().source
    if source.startswith("https://"):
        reviews = public_reviews(source)
    else:
        path = url2pathname(urlsplit(source).path) if source.startswith("file:///") else source
        html = ForumHTML()
        html.feed(Path(path).read_text(encoding="utf-8-sig"))
        reviews = html.reviews
    if not reviews or any(not r["fields"] for r in reviews):
        raise ValueError("Missing review content. Expand all official reviews and save the rendered HTML.")
    directory = Path("rebuttal")
    directory.mkdir(exist_ok=True)
    data = directory / "reviews.json"
    documents = {data: json.dumps(reviews, ensure_ascii=False, indent=2)}
    for index, review in enumerate(json.loads(documents[data]), 1):
        sections = [f"# {review['title']}"]
        for label, value in review["fields"].items():
            sections.append(f"## {label}\n\n{value}")
        documents[directory / f"review-{index}.md"] = "\n\n".join(sections) + "\n"
    if any(path.exists() for path in documents) or any(directory.glob("review-*.md")):
        raise ValueError("Review files already exist. Move the previous import before importing again.")
    for path, body in documents.items():
        path.write_text(body, encoding="utf-8")
    print(f"Imported {len(reviews)} reviews into {directory}")


if __name__ == "__main__":
    main()

