#!/usr/bin/env python3
"""Gera o blog estático do ALCOVA.

Uso:  python3 tools/build_blog.py

Lê content/blog/*.html (front matter "chave: valor" + linha "---" + corpo HTML)
e gera:
  blog/<slug>/index.html   uma página por artigo
  blog/index.html          lista de artigos
  blog/feed.xml            RSS
  sitemap.xml, robots.txt  na raiz

Para publicar um artigo novo: crie content/blog/<slug>.html, rode o script,
faça commit e push. O GitHub Pages publica em ~1 minuto.
"""
from __future__ import annotations

import html
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "blog"
OUT = ROOT / "blog"
BASE = "https://arthurvalle1.github.io/alcova-legal/"
PLAY = "https://play.google.com/store/apps/details?id=app.alcova"
STATIC_PAGES = ["", "legal.html", "privacy.html", "terms.html", "delete.html"]

MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
          "agosto", "setembro", "outubro", "novembro", "dezembro"]


def play_link(slug: str, medium: str) -> str:
    ref = f"utm_source%3Dblog%26utm_medium%3D{medium}%26utm_campaign%3D{slug}"
    return f"{PLAY}&amp;referrer={ref}"


def parse(path: pathlib.Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    meta["slug"] = path.stem
    meta["body"] = body.strip()
    meta["date_obj"] = date.fromisoformat(meta["date"])
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    meta["minutes"] = max(1, round(words / 220))
    return meta


def fmt_date(d: date) -> str:
    return f"{d.day} de {MONTHS[d.month - 1]} de {d.year}"


HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0e0a0c">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="ALCOVA">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Blog do ALCOVA" href="{base}blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/site.css">
{jsonld}
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{rel}">ALC<span>O</span>VA</a>
    <nav class="nav">
      <a href="{rel}#como-funciona">Como funciona</a>
      <a href="{rel}blog/">Blog</a>
      <a class="btn" href="{play_header}">Baixar</a>
    </nav>
  </div>
</header>
"""

FOOT = """
<footer>
  <div class="wrap">
    <div>© {year} ART Produções e Distribuição Ltda. · Conteúdo para maiores de 18 anos.</div>
    <div><a href="{rel}">Início</a><a href="{rel}blog/">Blog</a><a href="{rel}privacy.html">Privacidade</a><a href="{rel}terms.html">Termos</a><a href="{rel}delete.html">Excluir conta</a></div>
  </div>
</footer>
</body>
</html>
"""


def article_page(p: dict, all_posts: list[dict]) -> str:
    url = f"{BASE}blog/{p['slug']}/"
    e = html.escape
    jsonld = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting",'
        f'"headline":{_j(p["title"])},"description":{_j(p["description"])},'
        f'"datePublished":"{p["date"]}","dateModified":"{p["date"]}","inLanguage":"pt-BR",'
        f'"mainEntityOfPage":"{url}","image":"{BASE}assets/og.png",'
        f'"keywords":{_j(p.get("keywords", ""))},'
        '"author":{"@type":"Organization","name":"ALCOVA"},'
        '"publisher":{"@type":"Organization","name":"ART Produções e Distribuição Ltda."}}</script>'
    )
    related = [q for q in all_posts if q["slug"] != p["slug"]][:3]
    rel_html = "".join(
        f'<li><a href="../{q["slug"]}/">{e(q["title"])}</a></li>' for q in related
    )
    return (
        HEAD.format(
            title=e(p["title"]) + " | ALCOVA", description=e(p["description"]), url=url,
            og_type="article", og_title=e(p["title"]), base=BASE, rel="../../", jsonld=jsonld,
            play_header=play_link(p["slug"], "header"),
        )
        + f"""<main>
<article class="post">
  <div class="kicker">{e(p.get('kicker', 'Blog'))}</div>
  <h1>{e(p['title'])}</h1>
  <div class="post-meta">{fmt_date(p['date_obj'])} · {p['minutes']} min de leitura</div>
{p['body']}
  <div class="cta-box">
    <h3>Escolha sua personagem. A primeira confissão é por nossa conta.</h3>
    <p>ALCOVA: ficção interativa adulta (+18) com IA, em português. Catálogo estilo app de encontros, sagas com começo, meio e fim.</p>
    <a class="btn" href="{play_link(p['slug'], 'article_cta')}">▶ Baixar no Google Play</a>
  </div>
</article>
<aside class="related">
  <h3>Leia também</h3>
  <ul>{rel_html}</ul>
</aside>
</main>"""
        + FOOT.format(year=date.today().year, rel="../../")
    )


def _j(s: str) -> str:
    import json
    return json.dumps(s, ensure_ascii=False)


def index_page(posts: list[dict]) -> str:
    e = html.escape
    cards = "\n".join(
        f"""  <a class="post-card" href="{p['slug']}/">
    <div class="kicker">{e(p.get('kicker', 'Blog'))} · {p['minutes']} min</div>
    <h3>{e(p['title'])}</h3>
    <p>{e(p['description'])}</p>
  </a>"""
        for p in posts
    )
    return (
        HEAD.format(
            title="Blog do ALCOVA — ficção interativa, personagens de IA e histórias para adultos",
            description="Guias, comparativos e bastidores sobre ficção interativa com IA, personagens em português e as sagas do ALCOVA.",
            url=f"{BASE}blog/", og_type="website", og_title="Blog do ALCOVA", base=BASE,
            rel="../", jsonld="", play_header=play_link("blog_index", "header"),
        )
        + f"""<main>
<section>
  <div class="wrap">
    <h1 style="font-size:clamp(34px,5vw,50px)">Blog do ALCOVA</h1>
    <p class="sub">Ficção interativa, personagens de IA em português e os bastidores das nossas sagas.</p>
    <div class="post-list">
{cards}
    </div>
  </div>
</section>
</main>"""
        + FOOT.format(year=date.today().year, rel="../")
    )


def feed(posts: list[dict]) -> str:
    e = html.escape
    items = "".join(
        f"""<item><title>{e(p['title'])}</title><link>{BASE}blog/{p['slug']}/</link>
<guid>{BASE}blog/{p['slug']}/</guid><pubDate>{p['date_obj'].strftime('%a, %d %b %Y')} 12:00:00 -0300</pubDate>
<description>{e(p['description'])}</description></item>
"""
        for p in posts
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>Blog do ALCOVA</title><link>{BASE}blog/</link><language>pt-BR</language>
<description>Ficção interativa com IA, em português, para adultos.</description>
{items}</channel></rss>
"""


def sitemap(posts: list[dict]) -> str:
    today = date.today().isoformat()
    urls = [(BASE + s, today, "1.0" if s == "" else "0.3") for s in STATIC_PAGES]
    urls.append((BASE + "blog/", today, "0.8"))
    urls += [(f"{BASE}blog/{p['slug']}/", p["date"], "0.7") for p in posts]
    body = "".join(
        f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n"
        for u, d, pr in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}</urlset>\n")


def main() -> None:
    posts = sorted((parse(f) for f in SRC.glob("*.html")),
                   key=lambda p: (p["date_obj"], p["slug"]), reverse=True)
    OUT.mkdir(exist_ok=True)
    for p in posts:
        d = OUT / p["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(article_page(p, posts), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(posts), encoding="utf-8")
    (OUT / "feed.xml").write_text(feed(posts), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(posts), encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    print(f"{len(posts)} artigos gerados.")


if __name__ == "__main__":
    main()
