#!/usr/bin/env python3
"""Tests automatiques de « Sous le tapis » (depuis la 10.81).

Ouvre l'appli HORS LIGNE dans un navigateur sans fenêtre, chaque scénario dans
un profil vierge et jetable : aucune donnée réelle n'est lue ni touchée, rien
n'est envoyé à Firebase. À lancer avant chaque publication :

    python3 tests/run.py              # teste essai.html (le banc)
    python3 tests/run.py index.html   # teste l'appli publiée

Besoin : Python 3, le module playwright (pip install playwright) et Chrome
(chemin dans CHROME ci-dessous, sinon `playwright install chromium`).
Ajouter un scénario : une fonction async `t_nom(pg)` qui lève AssertionError
si quelque chose cloche ; elle est trouvée et lancée toute seule.
"""
import asyncio, os, sys, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")

# --- petits outils ---------------------------------------------------------
async def js(pg, code, arg=None):
    return await pg.evaluate(code, arg)

async def texts(pg, sel):
    return await pg.evaluate("s => [...document.querySelectorAll(s)].map(e => e.innerText.replace(/\\s+/g, ' ').trim())", sel)

async def new_list(pg, title, memo=False):
    """Crée une liste (ou un mémo) et renvoie son identifiant."""
    return await js(pg, """([t, memo]) => { addCategory(t); const c = DATA[DATA.length - 1];
        if(memo) setCoursesList(c.id, true); renderAll(); return c.id; }""", [title, memo])

async def add_tasks(pg, cat_id, *titles):
    await js(pg, """([id, ts]) => { const c = DATA.find(x => x.id === id);
        ts.forEach(t => addQuickTask(c, t)); renderAll(); }""", [cat_id, list(titles)])

def check(cond, msg):
    if not cond: raise AssertionError(msg)

URGENT = "#urgentBanner .urgent-list li"
WAITING = "#waitingSection .item"

# --- scénarios -------------------------------------------------------------
async def t_ouverture(pg):
    check(await js(pg, "typeof DATA !== 'undefined' && typeof renderAll === 'function'"), "l'appli ne démarre pas")

async def t_cocher_compte(pg):
    c = await new_list(pg, "Maison")
    await add_tasks(pg, c, "Réparer la porte")
    avant = await js(pg, "getWeekDoneCount()")
    await pg.locator(f"#cat-{c} .item input[type=checkbox], #cat-{c} .item .check").first.click(force=True)
    await pg.wait_for_timeout(300)
    check(await js(pg, "getWeekDoneCount()") == avant + 1, "cocher n'ajoute pas 1 au compteur")
    await pg.reload(); await pg.wait_for_timeout(800)
    check(await js(pg, "getWeekDoneCount()") == avant + 1, "la coche est perdue au rechargement")

async def t_urgent_triangle(pg):
    c = await new_list(pg, "Boulot")
    await add_tasks(pg, c, "Appeler le notaire")
    await js(pg, "k => { overrides = loadOverrides(); overrides[k] = Object.assign(overrides[k] || {}, { urgent:true }); saveOverrides(overrides); renderAll(); }", f"{c}:0")
    check(len(await texts(pg, URGENT)) == 1, "la tâche urgente n'est pas dans la case urgente")
    await pg.locator(URGENT + " .urgent-btn").first.click(force=True)
    await pg.wait_for_timeout(300)
    check(len(await texts(pg, URGENT)) == 0, "le triangle ne retire pas l'urgence")

async def t_en_cours_aller_retour(pg):
    c = await new_list(pg, "Papiers")
    await add_tasks(pg, c, "Envoyer le formulaire")
    avant = await js(pg, "getWeekDoneCount()")
    await js(pg, "k => sendToWaiting(k, '')", f"{c}:0")
    check(any("Envoyer le formulaire" in t for t in await texts(pg, WAITING)), "pas dans « En cours »")
    check(await js(pg, "getWeekDoneCount()") == avant + 1, "l'envoi en cours ne compte pas")
    check(len(await texts(pg, f"#cat-{c} .item")) == 0, "toujours visible dans sa liste")
    await js(pg, "k => bringBackFromWaiting(k)", f"{c}:0")
    check(len(await texts(pg, f"#cat-{c} .item")) == 1, "le retour dans la liste ne marche pas")

async def t_relance_rentre(pg):
    c = await new_list(pg, "Suivis")
    await add_tasks(pg, c, "Relancer la banque", "Attendre le devis")
    await js(pg, """id => { sendToWaiting(id + ':0', addDaysISO(todayISO(), 7)); sendToWaiting(id + ':1', addDaysISO(todayISO(), 7));
        overrides = loadOverrides(); overrides[id + ':0'].relance = todayISO(); saveOverrides(overrides); renderAll(); }""", c)
    await pg.wait_for_timeout(300)
    liste = await texts(pg, f"#cat-{c} .item")
    check(len(liste) == 1 and await texts(pg, f"#cat-{c} .item .status-relance"), f"la relance du jour n'est pas rentrée dans sa liste : {liste}")
    check(len(await texts(pg, URGENT)) == 1, "la relance du jour n'est pas urgente")
    check(any("Attendre le devis" in t for t in await texts(pg, WAITING)), "une relance future a quitté « En cours »")
    await pg.locator(URGENT + " .urgent-btn").first.click(force=True)
    await pg.wait_for_timeout(300)
    check(len(await texts(pg, URGENT)) == 0, "le triangle ne rend pas la relance non urgente")
    check(len(await texts(pg, f"#cat-{c} .item .status-relance")) == 0, "l'étiquette Relance reste")
    avant = await js(pg, "getWeekDoneCount()")
    await js(pg, "k => sendToWaiting(k, addDaysISO(todayISO(), 14))", f"{c}:0")
    check(await js(pg, "getWeekDoneCount()") == avant + 1, "le renvoi en cours ne compte pas")
    check(len(await texts(pg, f"#cat-{c} .item")) == 0, "renvoyée, elle reste dans sa liste")

async def t_memo_detail(pg):
    c = await new_list(pg, "Courses", memo=True)
    await js(pg, "id => { addCoursesQuick(DATA.find(x => x.id === id), 'Pain\\nLait x2\\nPâtes fraîches de chez le traiteur du coin'); renderAll(); }", c)
    items = f"#cat-{c} .courses-item"
    check(len(await texts(pg, items)) == 3, "les 3 articles ne sont pas là")
    for i, valider in enumerate(["enter", "save", "outside"]):
        await pg.locator(f"{items}:not(.editing) .item-text").nth(i).dblclick()
        await pg.wait_for_timeout(250)
        note = pg.locator(".courses-edit-note")
        await note.click(); await note.type("bio")
        if valider == "enter": await pg.keyboard.press("Enter")
        elif valider == "save": await pg.locator(".courses-item.editing .edit-save").click()
        else: await pg.mouse.click(5, 5)
        await pg.wait_for_timeout(300)
        n = len(await texts(pg, items))
        check(n == 3, f"modifier le détail ({valider}) donne {n} articles au lieu de 3")
    t = await texts(pg, items)
    check("bio" in t[0] and "bio" in t[1], f"le détail n'est pas enregistré : {t}")
    check("bio" not in t[2], "un clic à côté devrait annuler")
    ombre = await js(pg, "s => getComputedStyle(document.querySelector(s)).boxShadow", items + ":first-child")
    check("inset" in ombre, "le filet au-dessus du premier article a disparu")

async def t_effacer_tache(pg):
    c = await new_list(pg, "Brouillon")
    await add_tasks(pg, c, "A", "B")
    await pg.locator(f"#cat-{c} .item .delete-btn").first.click(force=True)
    await pg.wait_for_timeout(300)
    check(len(await texts(pg, f"#cat-{c} .item")) == 1, "effacer une tâche ne marche pas")

# --- lancement --------------------------------------------------------------
async def main():
    page = sys.argv[1] if len(sys.argv) > 1 else "essai.html"
    url = (ROOT / page).as_uri()
    tests = [(n, f) for n, f in globals().items() if n.startswith("t_") and callable(f)]
    ok = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--no-sandbox"])
        for name, fn in tests:
            ctx = await browser.new_context(viewport={"width": 1300, "height": 900})
            pg = await ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            try:
                await pg.goto(url); await pg.wait_for_timeout(1200)
                await fn(pg)
                check(not errs, "erreur JavaScript : " + "; ".join(errs[:3]))
                print(f"  ok      {name[2:]}"); ok += 1
            except Exception as e:
                print(f"  ÉCHEC   {name[2:]} — {e}")
            await ctx.close()
        await browser.close()
    print(f"\n{ok}/{len(tests)} réussis sur {page}")
    sys.exit(0 if ok == len(tests) else 1)

asyncio.run(main())
