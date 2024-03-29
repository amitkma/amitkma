import feedparser
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

TOKEN = os.environ.get("SIMONW_TOKEN", "")


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- START {} \-\->.*<!\-\- END {} \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- START {} -->\n{}\n<!-- END {} -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse("https://amitkma.github.io/posts/index.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog_posts", entries_md)

    readme.open("w").write(rewritten)