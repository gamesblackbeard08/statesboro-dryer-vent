import json, html, shutil
from pathlib import Path
from datetime import date
ROOT=Path(__file__).parent
DIST=ROOT/'dist'
site=json.loads((ROOT/'content/site.json').read_text())
pages=[]
for p in sorted((ROOT/'content/pages').glob('*.json')):
    pages.append(json.loads(p.read_text()))
by_slug={p['slug']:p for p in pages}

def esc(x): return html.escape(str(x), quote=True)
def url_for(slug):
    base=site['site_url'].rstrip('/')
    return base+'/' if not slug else base+'/'+slug.strip('/')+'/'
def page_path(slug): return DIST/'index.html' if not slug else DIST/slug/'index.html'
def rel_href(slug): return '/' if not slug else f'/{slug}/'
def schema(page):
    data={"@context":"https://schema.org","@type":"WebPage","name":page['title'],"url":url_for(page['slug']),"description":page['description'],"isPartOf":{"@type":"WebSite","name":site['brand'],"url":site['site_url'].rstrip('/')+'/'}}
    return json.dumps(data,separators=(',',':'))
def render(page):
    noindex='' if site.get('production_ready') else '<meta name="robots" content="noindex,nofollow">'
    nav=''.join([f'<a href="{h}">{t}</a>' for h,t in [('/dryer-vent-cleaning/','Cleaning'),('/dryer-vent-repair/','Repair'),('/clogged-dryer-vent/','Problems'),('/dryer-vent-cleaning-cost/','Guides'),('/about/','About'),('/contact/','Contact')]])
    sections=''.join([f'<section class="section"><h2>{esc(s["h2"])}</h2><p>{esc(s["body"])}</p></section>' for s in page.get('sections',[])])
    faqs=''.join([f'<div class="faq"><h3>{esc(f["q"])}</h3><p>{esc(f["a"])}</p></div>' for f in page.get('faqs',[])])
    faq_block=f'<section class="section"><h2>Frequently asked questions</h2>{faqs}</section>' if faqs else ''
    related=[]
    for slug in page.get('related',[]):
        if slug in by_slug: related.append(f'<a class="card" href="{rel_href(slug)}"><strong>{esc(by_slug[slug]["h1"])}</strong><span>{esc(by_slug[slug]["description"])}</span></a>')
    related_block=f'<section class="section"><h2>Related dryer vent topics</h2><div class="cards">{"".join(related)}</div></section>' if related else ''
    prelaunch=''
    if not site.get('production_ready'):
        prelaunch='<div class="notice"><strong>Prelaunch build:</strong> This deployment is intentionally set to noindex. Add the final domain and verified contact details in <code>content/site.json</code> before switching <code>production_ready</code> to true.</div>'
    contact=''
    if site.get('phone') or site.get('email'):
        bits=[]
        if site.get('phone'): bits.append(f'<span class="pill">{esc(site["phone"])}</span>')
        if site.get('email'): bits.append(f'<span class="pill">{esc(site["email"])}</span>')
        contact=''.join(bits)
    crumb='Home' if not page['slug'] else f'<a href="/">Home</a> &rsaquo; {esc(page["h1"])}'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(page['title'])}</title><meta name="description" content="{esc(page['description'])}">{noindex}<link rel="canonical" href="{esc(url_for(page['slug']))}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(page['title'])}"><meta property="og:description" content="{esc(page['description'])}"><meta property="og:url" content="{esc(url_for(page['slug']))}"><link rel="stylesheet" href="/assets/css/styles.css"><script type="application/ld+json">{schema(page)}</script></head><body><header class="site-header"><div class="wrap nav"><a class="brand" href="/">{esc(site['brand'])}</a><nav class="nav-links" aria-label="Primary">{nav}</nav></div></header><main><div class="wrap breadcrumb">{crumb}</div><section class="hero"><div class="wrap"><div class="eyebrow">{esc(site['market'])}</div><h1>{esc(page['h1'])}</h1><p class="lead">{esc(page['intro'])}</p>{contact}</div></section><div class="wrap">{prelaunch}<div class="content-grid"><article>{sections}{faq_block}{related_block}</article><aside class="sidebar"><div class="sidebar-box"><strong>Explore the site</strong><ul><li><a href="/dryer-vent-cleaning/">Dryer vent cleaning</a></li><li><a href="/dryer-vent-repair/">Repair & installation</a></li><li><a href="/clogged-dryer-vent/">Clogged vent guide</a></li><li><a href="/dryer-vent-cleaning-cost/">Cost factors</a></li><li><a href="/how-often-clean-dryer-vent/">Cleaning frequency</a></li></ul></div></aside></div></div></main><footer class="site-footer"><div class="wrap footer-grid"><div><strong>{esc(site['brand'])}</strong><p>{esc(site['tagline'])}</p><p class="small">{esc(site['footer_note'])}</p></div><div><strong>Services</strong><p><a href="/dryer-vent-cleaning/">Cleaning</a><br><a href="/dryer-vent-repair/">Repair</a><br><a href="/commercial-dryer-vent-cleaning/">Commercial</a></p></div><div><strong>Site</strong><p><a href="/about/">About</a><br><a href="/contact/">Contact</a><br><a href="/privacy/">Privacy</a></p></div></div></footer><script src="/assets/js/main.js" defer></script></body></html>'''

if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
shutil.copytree(ROOT/'assets', DIST/'assets')
for p in pages:
    out=page_path(p['slug']); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(render(p))
# sitemap only when production ready; harmless but noindex on test deployment
urls=''.join([f'<url><loc>{esc(url_for(p["slug"]))}</loc><lastmod>{date.today().isoformat()}</lastmod></url>' for p in pages])
(DIST/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
robots='User-agent: *\nDisallow: /\n' if not site.get('production_ready') else f'User-agent: *\nAllow: /\n\nSitemap: {site["site_url"].rstrip("/")}/sitemap.xml\n'
(DIST/'robots.txt').write_text(robots)
(DIST/'404.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/css/styles.css"><title>Page not found</title></head><body><main class="wrap section"><h1>Page not found</h1><p><a href="/">Return to the homepage</a></p></main></body></html>')
print(f'Built {len(pages)} pages into {DIST}')
