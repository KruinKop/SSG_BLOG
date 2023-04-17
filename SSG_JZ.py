from jinja2 import Environment, FileSystemLoader
import parsing as p
from rich import print
from pathlib import Path
import os

paginas = []
nav = []
content = []
links = []

blogs = []
blog_content = []
blog_preview = []
blog_links = []

hashtags = {}

environment = Environment(loader=FileSystemLoader("templates/"))
page_template = environment.get_template("pagina.html")
blog_template = environment.get_template("blog.html")
tag_template = environment.get_template("tags.html")

basePath_pages = Path("./pages/")
alleBestanden = basePath_pages.iterdir()
for bestand in alleBestanden:
    with open(bestand, "r") as f:
        paginas.append(p.parseMeta(f))
    with open(bestand, "r") as f:
        content.append(p.parseBody(f))

basePath_blogs = Path("./blogs/")
alleBestanden = basePath_blogs.iterdir()
for bestand in alleBestanden:
    with open(bestand, "r") as f:
        blogs.append(p.parseMeta(f, "blog"))
    with open(bestand, "r") as f:
        blog_content.append(p.parseBody(f))
    with open(bestand, "r") as f:
        blog_preview.append(p.parseBody(f, "preview"))

rootPad = "https://kruinkop.github.io/"

for i in range(0, len(paginas)):
    if paginas[i]["pagina"] == "index":
        for navItem in paginas[i]["nav"]:
            nav.append(navItem)
            newPage = navItem.replace(" ", "_")
            link = rootPad + "SSG_BLOG/" + newPage + ".html"
            links.append(link)

# het aanmaken van alle blogposts gebeurt hieronder

for i in range(0, len(blogs)):
    blognaam = blogs[i]["blog"].replace(" ", "_")
    bestandsnaam = "./SSG_BLOG/" + blognaam + ".html"
    bloglink = rootPad + "SSG_BLOG/" + blognaam + ".html"
    blog_links.append(bloglink)

    #tags selecteren

    hashtags.setdefault(blogs[i]["tag"], []).append((blogs[i]["blog"], bloglink))

    context = {
        "links": links,
        "navigatie": nav,
        "filename": blogs[i]["blog"],
        "post": blog_content[i],
    }    
      
    with open(bestandsnaam, mode="w", encoding="utf-8") as blog:
        blog.write(blog_template.render(context))
        print(f"... wrote {bestandsnaam}")

# het aanmaken van de site index gebeurt hieronder

for i in range(0, len(paginas)):
    paginanaam = paginas[i]["pagina"].replace(" ", "_")
    bestandsnaam = "./SSG_BLOG/" + paginanaam + ".html"

    context = {
        "links": links,
        "navigatie": nav,
        "filename": paginas[i]["pagina"],
        "post": content[i],
        "blogs": blog_preview,
        "blog_links" : blog_links,
        "hashtags": hashtags
    }  
      
    with open(bestandsnaam, mode="w", encoding="utf-8") as pagina:
        pagina.write(page_template.render(context))
        print(f"... wrote {bestandsnaam}")
