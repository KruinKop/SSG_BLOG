import frontmatter
import marko 

def parseBody(f, type="content"):
    match type:
        case "content":
            file = f.read()[3 :]
            limit = file.find('---')
            body = file[limit+3 :]
            post = marko.convert(body)
            return post
        case "preview":
            file = f.read()[3 :]
            limit = file.find('---')
            body = file[limit+3:limit+203]
            body += "..."
            post = marko.convert(body)
            return post


def parseMeta(f, type="page"):
    meta = {}
    match type:
        case "page":
            md = frontmatter.load(f)
            meta["pagina"] = md["pagina"]
            meta["nav"] = md["nav"]
            meta["post"] = md["post"]
            meta["auteur"] = md["auteur"]
        case "blog":
            md = frontmatter.load(f)
            meta["blog"] = md["blog"]
            meta["nav"] = md["nav"]
            meta["tag"] = md["tag"]
            meta["auteur"] = md["auteur"]
    return meta
