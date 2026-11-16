#!/usr/bin/env python3
"""Tests de la copie gardée sur l'appareil (sw.js, depuis la 11.2).

Sert une copie jetable du dépôt sur un petit serveur local, et vérifie dans un navigateur sans fenêtre :
première visite (la copie se fait), ouverture sans réseau, nouvelle version à la 2e ouverture, banc d'essai
jamais servi depuis la copie, arrêt à distance (ARRET = true).

    python3 tests/copie.py
"""
import asyncio, os, sys, pathlib, shutil, tempfile, threading, functools, http.server, socketserver
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")

def check(cond, msg):
    if not cond: raise AssertionError(msg)

class Calme(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

async def version(pg): return await pg.evaluate("document.querySelector('.version-tag').textContent")
async def copies(pg): return await pg.evaluate("caches.keys().then(async ks => { const out = []; for(const k of ks) for(const r of await (await caches.open(k)).keys()) out.push(r.url.replace(location.origin, '')); return out; })")
async def inscrits(pg): return await pg.evaluate("navigator.serviceWorker.getRegistrations().then(rs => rs.map(r => r.scope.replace(location.origin, '')))")
async def attendre(pg, expr, quoi, tours=60):
    """expr : une expression JS (promesse acceptée) ; on attend qu'elle soit vraie, 15 s au plus."""
    for _ in range(tours):
        if await pg.evaluate(expr): return
        await pg.wait_for_timeout(250)
    raise AssertionError(quoi)
async def ouvrir(pg, url, attente=900):
    await pg.goto(url); await pg.wait_for_timeout(attente)
    check(await pg.evaluate("typeof DATA !== 'undefined' && typeof renderAll === 'function'"), f"l'appli ne démarre pas ({url})")

async def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="sltapis-copie-"))
    for n in os.listdir(ROOT):
        if n in (".git", "archives", "tests"): continue
        (shutil.copytree if (ROOT / n).is_dir() else shutil.copy)(ROOT / n, tmp / n)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Calme, directory=str(tmp)))
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    ok = True
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--no-sandbox"])
            ctx = await b.new_context(viewport={"width": 390, "height": 800})
            await ctx.route("**/*gstatic.com/**", lambda r: r.abort())
            await ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
            pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            etapes = []
            def etape(nom): etapes.append(nom); print(f"  ok      {nom}", flush=True)

            # 1. première visite : rien n'est encore gardé ; la copie se fait au calme, après l'ouverture
            await ouvrir(pg, base + "/")
            v0 = await version(pg)
            await attendre(pg, "navigator.serviceWorker.getRegistrations().then(rs => rs.some(r => r.active))", "la copie ne s'inscrit pas")
            await pg.wait_for_timeout(800)
            check(await inscrits(pg) == ["/"], f"inscription inattendue : {await inscrits(pg)}")
            check("/" in await copies(pg), f"la page n'est pas gardée dès la première visite : {await copies(pg)}")
            etape("première visite : la page est gardée")

            # 2. sans réseau : l'appli s'ouvre depuis la copie (adresse du dossier, index.html, lien d'invitation)
            await ctx.set_offline(True)
            await ouvrir(pg, base + "/"); check(await version(pg) == v0, "mauvaise version sans réseau")
            await ouvrir(pg, base + "/index.html")
            await ouvrir(pg, base + "/?invitation=ABCD2345")
            check(await pg.evaluate("Object.keys(localStorage).some(k => /invitation/.test(k) && localStorage.getItem(k).includes('ABCD2345'))"), "le code d'un lien d'invitation n'est pas retenu")
            await ctx.set_offline(False)
            etape("sans réseau : l'appli s'ouvre depuis la copie")

            # 3. une nouvelle version est publiée : l'ancienne à la 1re ouverture, la nouvelle à la suivante
            page = tmp / "index.html"; page.write_text(page.read_text().replace(f'<span class="version-tag">{v0}</span>', '<span class="version-tag">v99.9</span>'))
            await ouvrir(pg, base + "/", 1500); check(await version(pg) == v0, "la 1re ouverture après publication devrait encore montrer l'ancienne version")
            await ouvrir(pg, base + "/"); check(await version(pg) == "v99.9", f"la nouvelle version n'arrive pas à la 2e ouverture ({await version(pg)})")
            await ouvrir(pg, base + "/index.html"); check(await version(pg) == "v99.9", "index.html et l'adresse du dossier ne montrent pas la même version")
            etape("nouvelle version : à la deuxième ouverture")

            # 4. les données ne passent pas par la copie : une tâche ajoutée est toujours là après rechargement
            await pg.evaluate("() => { addCategory('Copie'); const c = DATA[DATA.length - 1]; addQuickTask(c, 'Toujours là'); renderAll(); }")
            await ouvrir(pg, base + "/")
            check(await pg.evaluate("[...document.querySelectorAll('.item-title')].some(e => e.textContent.includes('Toujours là'))"), "une tâche ajoutée a disparu après rechargement")
            etape("les listes ne sont pas touchées")

            # 5. le banc vient toujours du site : un changement s'y voit dès la 1re ouverture ; l'inscription
            #    propre au banc (essai du 16/11/2026) est retirée
            await pg.evaluate("navigator.serviceWorker.register('sw.js', { scope: './essai.html' })")
            banc = tmp / "essai.html"; banc.write_text(banc.read_text().replace(f'<span class="version-tag">{v0}</span>', '<span class="version-tag">v77.7</span>'))
            await ouvrir(pg, base + "/essai.html?demo"); check(await version(pg) == "v77.7", "le banc est servi depuis une copie")
            banc.write_text(banc.read_text().replace("v77.7", "v77.8"))
            await ouvrir(pg, base + "/essai.html?demo"); check(await version(pg) == "v77.8", "un changement du banc ne se voit pas tout de suite")
            await attendre(pg, "navigator.serviceWorker.getRegistrations().then(rs => rs.length === 1 && /\\/$/.test(rs[0].scope))", "l'ancienne inscription du banc n'est pas retirée")
            check(not any("essai" in c for c in await copies(pg)), f"le banc est gardé dans la copie : {await copies(pg)}")
            etape("le banc vient toujours directement du site")

            # 6. arrêt à distance : ARRET = true publié → copie effacée, plus rien d'inscrit, l'appli marche toujours
            sw = tmp / "sw.js"; src = sw.read_text(); check("const ARRET = false;" in src, "ARRET introuvable dans sw.js")
            sw.write_text(src.replace("const ARRET = false;", "const ARRET = true;"))
            await ouvrir(pg, base + "/", 600)
            await attendre(pg, "navigator.serviceWorker.getRegistrations().then(rs => rs.length === 0)", "ARRET publié : l'inscription n'est pas retirée")
            await pg.wait_for_timeout(500)
            check(await copies(pg) == [], f"la copie n'est pas effacée : {await copies(pg)}")
            page.write_text(page.read_text().replace("v99.9", "v100.0"))
            await ouvrir(pg, base + "/", 600)
            check(await version(pg) == "v100.0", "après l'arrêt, la page ne vient plus directement du site")
            etape("arrêt à distance : copie effacée, l'appli vient de nouveau du site")

            check(not errs, "erreur JavaScript : " + "; ".join(errs[:3]))
            await b.close()
    except Exception as e:
        ok = False; print(f"  ÉCHEC   {e}")
    finally:
        srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)
    print("\ncopie sur l'appareil : " + ("tout est bon" if ok else "ÉCHEC"))
    sys.exit(0 if ok else 1)

asyncio.run(main())
