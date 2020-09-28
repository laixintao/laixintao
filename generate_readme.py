import sys
import requests
import lxml.html

URL = "https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day"

README = """
![{title}]({image_src})

*[{title}]({wiki_link})*
"""


def fetch_image():
    """
    return image url, and image title.
    """
    print("download image...")
    content = requests.get(URL).content
    html = lxml.html.fromstring(content)
    presentation_table = html.xpath("//table[@role='presentation']")[0]
    a_tag = presentation_table.xpath(".//a[@class='image']")[0]
    relative_link = a_tag.get("href")
    title = a_tag.get("title")
    image_src = a_tag.xpath("./img/@src")[0]
    print(f"{relative_link} {title} {image_src}")
    return relative_link, title, image_src


relative_link, title, image_src = fetch_image()

with open("readme.md", "r") as old_readme:
    if title in old_readme.read():
        print("Todays featured image not change!")
        sys.exit()

new_readme = README.format(
    title=title, image_src=image_src, wiki_link="wikipedia.org" + relative_link
)

print("new readme file generate... save...")
with open("readme.md", "w+") as f:
    f.write(new_readme)
