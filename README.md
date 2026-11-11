# ALCOVA — site, blog e kit de marketing

Site estático publicado via GitHub Pages: landing page, blog, páginas legais.

- `index.html` — landing page (SEO, FAQ, dados estruturados)
- `legal.html`, `privacy.html`, `terms.html`, `delete.html` — documentos legais (URLs mantidas)
- `blog/` — gerado; **não edite à mão**
- `content/blog/*.html` — fonte dos artigos (front matter + HTML)
- `tools/build_blog.py` — gera blog, RSS, `sitemap.xml` e `robots.txt`
- `marketing/` — plano de marketing e kits de execução (comece por `marketing/PLANO-DE-MARKETING.md`)

## Publicar um artigo novo

1. Crie `content/blog/<slug>.html` copiando um artigo existente (título, descrição, data, corpo).
2. Rode `python3 tools/build_blog.py`.
3. `git add -A && git commit -m "Artigo: ..." && git push`.
4. No Google Search Console, peça indexação da URL nova.
