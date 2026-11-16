#!/usr/bin/env python3
"""Mesure de fluidité de « Sous le tapis » (depuis la 11.1) : ouverture et défilement.

Hors ligne, profil jetable, données d'exemple (tests/donnees-exemple.json, ou DONNEES=/chemin/sauvegarde.json).
Le processeur est ralenti (4 fois par défaut) pour ressembler à un téléphone. À lancer avant / après un
changement qui touche au rendu, sur index.html (référence) et essai.html (banc) :

    python3 tests/mesure.py essai.html            # téléphone, processeur ralenti 4 fois
    python3 tests/mesure.py index.html 4 ordi     # ordinateur

Lecture : « tâches longues » = [début, durée] en ms des moments où l'appli ne répond pas (rien au-delà
du premier affichage, c'est le but) ; défilement : images par seconde et durée des images (16,7 ms = fluide).
Les chiffres valent pour comparer deux versions sur la même machine, pas dans l'absolu (pas de carte graphique ici).
"""
import asyncio, sys, json, pathlib, os, collections
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
DONNEES = os.environ.get("DONNEES", str(ROOT / "tests/donnees-exemple.json"))
LOAD = """d => { d = JSON.parse(d);
  const n = {}; d.lists.forEach(L => { if(L.owner) n[L.owner] = (n[L.owner] || 0) + 1; });
  const moi = Object.keys(n).sort((a, b) => n[b] - n[a])[0];
  if(moi) localStorage.setItem(Store.ns + "me", moi);
  Store.importModel(d); DATA.length = 0; reloadAllFromStorage(); renderAll(); }"""
INIT = """(() => { window.__p = { lt: [], paints: {}, firstCard: null, marks: [] };
  try { new PerformanceObserver(l => l.getEntries().forEach(e => __p.lt.push([Math.round(e.startTime), Math.round(e.duration)]))).observe({ type: "longtask", buffered: true }); } catch(e){}
  try { new PerformanceObserver(l => l.getEntries().forEach(e => __p.paints[e.name] = Math.round(e.startTime))).observe({ type: "paint", buffered: true }); } catch(e){}
  const mo = new MutationObserver(() => { if(!__p.firstCard && document.querySelector(".category")){ __p.firstCard = Math.round(performance.now()); requestAnimationFrame(() => requestAnimationFrame(() => __p.firstCardPainted = Math.round(performance.now()))); } });
  mo.observe(document, { childList: true, subtree: true });
})();"""
async def main():
    page = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    cpu = float(sys.argv[2]) if len(sys.argv) > 2 else 4
    vue = sys.argv[3] if len(sys.argv) > 3 else "tel"
    url = (ROOT / page).as_uri()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--no-sandbox", "--enable-gpu-benchmarking"])
        kw = dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True) if vue == "tel" else dict(viewport={"width": 1300, "height": 900})
        ctx = await b.new_context(**kw)
        await ctx.route("**/*gstatic.com/**", lambda r: r.abort())
        pg = await ctx.new_page()
        await pg.goto(url); await pg.wait_for_timeout(800)
        await pg.evaluate(LOAD, open(DONNEES).read()); await pg.wait_for_timeout(1500)
        await pg.add_init_script(INIT)
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
        res = []
        for i in range(3):
            await pg.reload(wait_until="load"); await pg.wait_for_timeout(4000)
            r = await pg.evaluate("() => ({ ...__p, dcl: Math.round(performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart), load: Math.round(performance.timing.loadEventEnd - performance.timing.navigationStart), cards: document.querySelectorAll('.category').length, items: document.querySelectorAll('.item').length, nodes: document.querySelectorAll('*').length, h: document.documentElement.scrollHeight })")
            res.append(r)
        for r in res:
            print(f"FP {r['paints'].get('first-paint')}  FCP {r['paints'].get('first-contentful-paint')}  1re case {r['firstCard']} (peinte {r.get('firstCardPainted')})  DCL {r['dcl']} load {r['load']}  tâches longues: {r['lt']}")
        r = res[-1]; print(f"cases {r['cards']} tâches {r['items']} nœuds {r['nodes']} hauteur {r['h']}px")
        # --- défilement : trace
        await pg.evaluate("() => scrollTo(0,0)"); await pg.wait_for_timeout(500)
        await b.start_tracing(page=pg, categories=["devtools.timeline", "disabled-by-default-devtools.timeline", "benchmark", "cc", "viz", "gpu"])
        h = r['h']
        await pg.evaluate("""h => new Promise(res => { window.__f = []; let last = performance.now(), run = true;
            const tick = t => { __f.push(t - last); last = t; if(run) requestAnimationFrame(tick); }; requestAnimationFrame(tick);
            chrome.gpuBenchmarking.smoothScrollBy(h, () => { chrome.gpuBenchmarking.smoothScrollBy(-h, () => { run = false; res(); }, 200, 300, 1, 'up', 2500); }, 200, 300, 1, 'down', 2500); })""", min(h, 9000))
        f = await pg.evaluate("() => __f")
        buf = await b.stop_tracing()
        ev = json.loads(buf)["traceEvents"]
        f = f[2:]
        f.sort()
        n = len(f)
        print(f"défilement : {n} images en {sum(f)/1000:.1f} s ({n*1000/sum(f):.0f} par seconde), médiane {f[n//2]:.1f} ms, p95 {f[int(n*.95)]:.1f} ms, max {f[-1]:.1f} ms, >25ms: {sum(1 for x in f if x > 25)}, >50ms: {sum(1 for x in f if x > 50)}")
        tot = collections.Counter(); cnt = collections.Counter()
        for e in ev:
            if e.get("ph") == "X" and e.get("name") in ("Paint", "Layout", "UpdateLayoutTree", "RasterTask", "FunctionCall", "EventDispatch", "PrePaint", "Layerize", "Commit", "CompositeLayers", "UpdateLayer", "TimerFire", "FireAnimationFrame", "ImageDecodeTask", "Decode Image", "IntersectionObserverController::computeIntersections", "HitTest", "ScrollLayer"):
                tot[e["name"]] += e.get("dur", 0) / 1000; cnt[e["name"]] += 1
        for k, v in tot.most_common(): print(f"   {k:28s} {v:8.1f} ms  ×{cnt[k]}")
        await b.close()
asyncio.run(main())
