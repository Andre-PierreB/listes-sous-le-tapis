#!/usr/bin/env python3
"""Tests automatiques de « Sous le tapis » (depuis la 10.81).

Ouvre l'appli HORS LIGNE dans un navigateur sans fenêtre, chaque scénario dans
un profil vierge et jetable : aucune donnée réelle n'est lue ni touchée, rien
n'est envoyé à Firebase. À lancer avant chaque publication :

    python3 tests/run.py              # teste essai.html (le banc)
    python3 tests/run.py index.html   # teste l'appli publiée
    python3 tests/run.py complet      # + comparateur jumeaux index ↔ essai (≈ 20 min)
    SEUL=duel python3 tests/run.py    # seulement les scénarios dont le nom contient « duel »

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

async def t_supprimer_liste_pleine(pg):
    """11.19 : « Supprimer la liste » dans la fenêtre de modification, liste pleine ; un seul ⌘Z remet tout."""
    autre = await new_list(pg, "Autre")
    await add_tasks(pg, autre, "Ne pas toucher")
    c = await new_list(pg, "À jeter")
    await add_tasks(pg, c, "Faite", "Urgente", "Partie", "Simple")
    keys = await js(pg, "id => getEffectiveItems(DATA.find(x => x.id === id)).map((b, i) => [b.t, id + ':' + i])", c)
    k = dict(keys)
    await js(pg, """k => { overrides = loadOverrides(); overrides[k.Urgente] = Object.assign(overrides[k.Urgente] || {}, { urgent:true });
        saveOverrides(overrides); sendToWaiting(k.Partie, ''); renderAll(); }""", k)
    await pg.locator(f'#cat-{c} li[data-key="{k["Faite"]}"] input[type=checkbox], #cat-{c} li[data-key="{k["Faite"]}"] .check').first.click(force=True)
    await pg.wait_for_timeout(300)
    avant = await js(pg, "getWeekDoneCount()")
    corb = await js(pg, "loadJSONKey(TRASH_KEY, []).length")
    check(len(await texts(pg, URGENT)) == 1 and len(await texts(pg, WAITING)) == 1, "préparation ratée")
    await js(pg, "id => { editingCategoryTitle = id; renderAll(); }", c)
    b = pg.locator(f"#cat-{c} .cat-remove")
    await b.click()
    t = await b.inner_text()
    check("4 tâches" in t, f"le premier clic doit annoncer ce qui sera effacé : {t!r}")
    check(await pg.locator(f"#cat-{c}").count() == 1, "le premier clic a déjà supprimé")
    await b.click(); await pg.wait_for_timeout(300)
    check(await pg.locator(f"#cat-{c}").count() == 0, "la liste est toujours là")
    check(len(await texts(pg, URGENT)) == 0, "sa tâche urgente reste dans la case urgente")
    check(len(await texts(pg, WAITING)) == 0, "sa tâche en cours reste dans « En cours »")
    check(await js(pg, "loadJSONKey(TRASH_KEY, []).length") == corb + 1, "la tâche faite n'est pas partie à la corbeille")
    check(await js(pg, "getWeekDoneCount()") == avant - 1, "compteur : seule la tâche en cours devait être décomptée (comme sa croix)")
    check(len(await texts(pg, f"#cat-{autre} .item")) == 1, "une autre liste a été touchée")
    await pg.keyboard.press("Control+z"); await pg.wait_for_timeout(400)
    check(await pg.locator(f"#cat-{c}").count() == 1, "⌘Z ne remet pas la liste")
    check(len(await texts(pg, f"#cat-{c} .item")) == 3, "⌘Z ne remet pas ses tâches")
    check(len(await texts(pg, URGENT)) == 1 and len(await texts(pg, WAITING)) == 1, "⌘Z ne remet pas l'urgente ou l'en cours")
    check(await js(pg, "getWeekDoneCount()") == avant, "⌘Z ne remet pas le compteur")
    check(await js(pg, "loadJSONKey(TRASH_KEY, []).length") == corb, "⌘Z ne vide pas la corbeille de ce qu'elle avait reçu")
    # mémo : articles effacés, jamais à la corbeille ; liste vide : un seul clic
    m = await new_list(pg, "Courses", memo=True)
    await js(pg, "id => { addCoursesQuick(DATA.find(x => x.id === id), 'Pain\\nLait'); editingCategoryTitle = id; renderAll(); }", m)
    b = pg.locator(f"#cat-{m} .cat-remove")
    await b.click()
    check("2 articles" in await b.inner_text(), "mémo : mauvaise annonce")
    await b.click(); await pg.wait_for_timeout(300)
    check(await pg.locator(f"#cat-{m}").count() == 0, "le mémo est toujours là")
    check(await js(pg, "loadJSONKey(TRASH_KEY, []).length") == corb, "un article de mémo est parti à la corbeille")
    v = await new_list(pg, "Vide")
    await js(pg, "id => { editingCategoryTitle = id; renderAll(); }", v)
    await pg.locator(f"#cat-{v} .cat-remove").click(); await pg.wait_for_timeout(300)
    check(await pg.locator(f"#cat-{v}").count() == 0, "une liste vide doit partir d'un seul clic")

async def t_copier_recoller(pg):
    """11.20 : « Copier » sans le titre ; recollé, l'œuf reste un œuf et l'urgente reste urgente."""
    c = await new_list(pg, "Source")
    await add_tasks(pg, c, "Simple", "Pressée")
    await js(pg, """id => { const c = DATA.find(x => x.id === id); insertItem(c, { t:"Couvée 1", egg:true }); insertItem(c, { t:"Couvée 2", egg:true });
        overrides = loadOverrides(); const k = getEffectiveItems(c).findIndex(b => b.t === "Pressée");
        overrides[id + ':' + k] = { urgent:true }; saveOverrides(overrides); renderAll(); }""", c)
    txt = await js(pg, "id => catTasksText(DATA.find(x => x.id === id)).join('\\n')", c)
    check("Source" not in txt, f"le titre est dans la copie : {txt!r}")
    check("[œuf]" in txt, f"les œufs ne sont pas marqués : {txt!r}")
    d = await new_list(pg, "Destination")
    got = await js(pg, """([id, txt]) => { const c = DATA.find(x => x.id === id); addPastedTasks(c, splitPastedTasks(txt)); renderAll();
        return getCatOrder(c).map(i => { const b = getEffectiveItems(c)[i]; return [b.t, !!b.egg, !!b.urgent]; }); }""", [d, txt])
    check([g[0] for g in got if g[1]] == ["Couvée 1", "Couvée 2"], f"œufs mal recollés : {got}")
    check(any(g[0] == "Pressée" and g[2] for g in got), f"l'urgente n'est plus urgente : {got}")
    check(all("[" not in g[0] for g in got), f"une marque est restée dans le texte : {got}")
    check(len(got) == 4, f"il devrait y avoir 4 tâches : {got}")

# --- 11.6 : cases fermées ---------------------------------------------------
async def t_case_entrouverte_se_referme(pg):
    """Bug 11.5 : une case redessinée juste après la sortie de la souris restait entrouverte."""
    c = await new_list(pg, "Courses", memo=True)
    await js(pg, "id => { const x = DATA.find(y => y.id === id); for(let i = 0; i < 12; i++) addQuickTask(x, 'Article ' + i); DATA.forEach(y => setFolded(y.id, true)); renderAll(); }", c)
    await pg.wait_for_timeout(400)
    b = await pg.locator(f"#cat-{c}").bounding_box()
    await pg.mouse.move(b["x"] + b["width"] / 2, b["y"] + 15, steps=4); await pg.wait_for_timeout(900)
    check(await js(pg, "id => document.getElementById('cat-' + id).classList.contains('peek')", c), "la case ne s'entrouvre pas au survol")
    await pg.mouse.move(5, 5, steps=2)
    await js(pg, "id => { addQuickTask(DATA.find(y => y.id === id), 'venu de la synchro'); renderAll(); }", c)
    await pg.wait_for_timeout(2500)
    check(not await js(pg, "id => document.getElementById('cat-' + id).classList.contains('peek')", c), "redessinée pendant le temps de grâce, la case reste entrouverte")

async def t_saisie_rapide_case_fermee(pg):
    """11.6 : une tâche ajoutée par la saisie rapide d'une liste fermée la laisse fermée (seule la bulle augmente)."""
    c = await new_list(pg, "Maison")
    await add_tasks(pg, c, "Trier la cave")
    await js(pg, "id => { setFolded(id, true); renderAll(); }", c)
    await pg.wait_for_timeout(300)
    await pg.locator(f"#cat-{c} .cat-quick").click(force=True)
    await pg.keyboard.type("Changer l'ampoule"); await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(500)
    check(await js(pg, "id => isFolded(id)", c), "la liste fermée s'est rouverte (punaisée)")
    check(await js(pg, "id => JSON.stringify(DATA.find(x => x.id === id)).includes(\"Changer l'ampoule\")", c) or "Changer l'ampoule" in " ".join(await texts(pg, f"#cat-{c} .item")), "la tâche n'est pas ajoutée")

# --- 11.1 : fluidité (rien de tout ça ne doit changer ce qu'on voit) ----------
async def _tel(pg):
    """Un téléphone (écran tactile, pas de survol) sur la même page, profil jetable."""
    ctx = await pg.context.browser.new_context(viewport={"width": 390, "height": 700}, has_touch=True, is_mobile=True)
    await ctx.route("**/*gstatic.com/**", lambda r: r.abort())
    tel = await ctx.new_page(); errs = []
    tel.on("pageerror", lambda e: errs.append(str(e)))
    await tel.goto(pg.url); await tel.wait_for_timeout(1200)
    return ctx, tel, errs

async def _doigt(cdp, kind, x=None, y=None):
    pts = [] if kind == "touchEnd" else [{"x": x, "y": y, "id": 1}]
    await cdp.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": pts})

async def t_glisser_au_doigt(pg):
    """Appui tenu sur la poignée : la tâche est saisie, la page ne défile pas, la tâche change de place.
    Sans appui tenu : la page défile et rien n'est saisi (10.35). Depuis la 11.1, l'écouteur qui bloque
    le défilement est sur les poignées, plus sur toute la page."""
    ctx, tel, errs = await _tel(pg)
    try:
        c = await new_list(tel, "Longue")
        await add_tasks(tel, c, *[f"Tâche {i}" for i in range(1, 31)])
        await tel.wait_for_timeout(300)
        cdp = await ctx.new_cdp_session(tel)
        ordre = lambda: tel.evaluate("id => [...document.querySelectorAll(`#cat-${id} .item .item-title`)].map(e => e.textContent.trim()).slice(0, 6)", c)
        avant = await ordre()
        grip = tel.locator(f"#cat-{c} .item .drag-handle").nth(1)
        await grip.evaluate("e => e.scrollIntoView({ block: 'center' })"); await tel.wait_for_timeout(300)
        bb = await grip.bounding_box(); x, y = bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2
        y0 = await js(tel, "scrollY")
        # 1) appui tenu puis glissé vers le bas
        await _doigt(cdp, "touchStart", x, y); await tel.wait_for_timeout(450)
        check(await js(tel, "!!dragState"), "l'appui tenu sur la poignée ne saisit pas la tâche")
        for k in range(1, 13):
            await _doigt(cdp, "touchMove", x, y + k * 10); await tel.wait_for_timeout(30)
        await tel.wait_for_timeout(200)
        check(abs(await js(tel, "scrollY") - y0) < 2, "la page défile pendant qu'on glisse une tâche au doigt")
        await _doigt(cdp, "touchEnd"); await tel.wait_for_timeout(500)
        check(not await js(tel, "!!dragState"), "le glisser ne se termine pas au lever du doigt")
        apres = await ordre()
        check(apres != avant and sorted(apres) == sorted(avant), f"la tâche glissée au doigt n'a pas changé de place : {avant} → {apres}")
        # 2) sans appui tenu : c'est un défilement ordinaire
        bb = await grip.bounding_box(); x, y = bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2
        y0 = await js(tel, "scrollY")
        await _doigt(cdp, "touchStart", x, y)
        for k in range(1, 13):
            await _doigt(cdp, "touchMove", x, y - k * 12); await tel.wait_for_timeout(16)
        check(not await js(tel, "!!dragState"), "un balayage sur la poignée saisit la tâche")
        await _doigt(cdp, "touchEnd"); await tel.wait_for_timeout(400)
        check(await js(tel, "scrollY") > y0 + 40, "balayer l'écran depuis une poignée ne fait plus défiler la page")
        check(not errs, "erreur JavaScript : " + "; ".join(errs[:3]))
    finally:
        await ctx.close()

async def t_tapis_au_clic(pg):
    """Le tapis n'est plus dessiné d'office (11.1) : au doigt, rien n'est préparé avant le clic ;
    le clic le déroule quand même, un second l'enroule."""
    ctx, tel, errs = await _tel(pg)
    try:
        c = await new_list(tel, "Tapis")
        await add_tasks(tel, c, "Une", "Deux")
        await tel.wait_for_timeout(3600)   # avant la 11.1 : préparé 3 s après l'ouverture
        check(await js(tel, "document.querySelector('.tapis-box canvas').width") <= 300, "le tapis est dessiné d'office sur téléphone")
        await tel.locator("header .eyebrow").click()
        await tel.wait_for_function("document.body.classList.contains('tapis-down') && document.querySelector('.tapis-box canvas').width > 300", timeout=15000)
        await tel.wait_for_timeout(2600)
        check(await js(tel, "getComputedStyle(document.querySelector('.tapis-box')).display") == "block", "le tapis ne se déroule pas")
        check("inset(0" in await js(tel, "document.querySelector('.tapis-box').style.clipPath") and await js(tel, "parseFloat(document.querySelector('.tapis-box').style.clipPath.split(' ')[2])") < 1, "le tapis ne se déroule pas jusqu'en bas")
        await tel.locator(".tapis-box").click(position={"x": 40, "y": 60}); await tel.wait_for_timeout(2600)
        check(await js(tel, "getComputedStyle(document.querySelector('.tapis-box')).display") == "none", "le tapis ne s'enroule pas")
        check(not errs, "erreur JavaScript : " + "; ".join(errs[:3]))
    finally:
        await ctx.close()

async def t_duel_au_repos(pg):
    """Le duel au repos n'est plus redessiné quand il est hors de l'écran (11.1), l'est de nouveau dès
    qu'il y revient, et toujours pendant un coup."""
    await js(pg, """() => { const n = { n: 0 }; window.__dessins = n; const f = CanvasRenderingContext2D.prototype.clearRect;
        CanvasRenderingContext2D.prototype.clearRect = function(){ if(this.canvas.classList.contains('duel-cv')) n.n++; return f.apply(this, arguments); }; }""")
    for i in range(10):   # assez de listes pour que le duel (créé en dernier, donc en bas) soit loin du haut de la page
        c = await new_list(pg, f"Liste {i}")
        await add_tasks(pg, c, *[f"Tâche {k}" for k in range(8)])
    await pg.locator(".add-category-btn").click(); await pg.locator(".nl-duel").click(); await pg.wait_for_timeout(800)
    cv = pg.locator(".duel-cv").first
    await cv.evaluate("e => e.scrollIntoView({ block: 'center' })"); await pg.wait_for_timeout(600)
    a = await js(pg, "__dessins.n"); await pg.wait_for_timeout(500); b = await js(pg, "__dessins.n")
    check(b - a > 10, f"le duel à l'écran n'est pas redessiné ({b - a} dessins en 0,5 s)")
    await js(pg, "scrollTo(0, 0)"); await pg.wait_for_timeout(600)
    loin = await cv.evaluate("e => { const r = e.getBoundingClientRect(); return r.bottom < -300 || r.top > innerHeight + 300; }")
    check(loin, "le test n'arrive pas à sortir le duel de l'écran")
    a = await js(pg, "__dessins.n"); await pg.wait_for_timeout(600); b = await js(pg, "__dessins.n")
    check(b - a <= 1, f"le duel hors de l'écran est encore redessiné ({b - a} dessins en 0,6 s)")
    await cv.evaluate("e => e.scrollIntoView({ block: 'center' })"); await pg.wait_for_timeout(600)
    a = await js(pg, "__dessins.n"); await pg.wait_for_timeout(500); b = await js(pg, "__dessins.n")
    check(b - a > 10, f"revenu à l'écran, le duel n'est plus redessiné ({b - a} dessins en 0,5 s)")
    # un coup lancé puis la page qui file ailleurs : le vol continue (le coup se termine)
    await pg.locator(".d-lancer").first.click(force=True); await pg.wait_for_timeout(150)
    await js(pg, "scrollTo(0, 0)")
    await pg.wait_for_timeout(300)
    a = await js(pg, "__dessins.n"); await pg.wait_for_timeout(400); b = await js(pg, "__dessins.n")
    check(b - a > 5, "hors de l'écran, un coup en vol n'avance plus")
    await pg.wait_for_function("!Duel.etat().busy", timeout=12000)

async def t_decalage_telephone(pg):
    """11.26 : au téléphone, le contenu des cases glisse de --ph-dx vers la gauche ; le champ des cases fermées,
    les titres et la flèche de tri restent où ils étaient ; les filets des mémos gardent leur départ. Ordi inchangé."""
    pos = """() => { const r = e => e ? Math.round(e.getBoundingClientRect().left * 10) / 10 : null;
        const l = [...document.querySelectorAll('.categories > .category:not(.courses):not(.chat-card):not(.duel-card)')].find(c => c.querySelector('ul.items > .item input'));
        const f = document.querySelector('.categories > .category.collapsed:not(.courses):not(.has-people) .cat-quick');
        const m = document.querySelector('.category.courses:not(.collapsed)');
        return { dx: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--ph-dx')) || 0,
          chk: r(l.querySelector('ul.items > .item input')), title: r(l.querySelector('.cat-title-group')), card: r(l),
          ul: getComputedStyle(l.querySelector('ul.items')).marginLeft, field: r(f),
          chkC: (b => b.left + b.width / 2)(l.querySelector('ul.items > .item input').getBoundingClientRect()),
          ordC: (b => b.left + b.width / 2)(l.querySelector(':scope > .cat-order svg').getBoundingClientRect()),
          dotC: m && (b => b.left + b.width / 2)(m.querySelector('.strike-dot').getBoundingClientRect()),
          mordC: m && (b => b.left + b.width / 2)(m.querySelector(':scope > .cat-order svg').getBoundingClientRect()),
          bulC: (e => e && (b => b.left + b.width / 2)(e.getBoundingClientRect()))(document.querySelector('.urgent-list .urgent-bullet')),
          memoLi: m && r(m.querySelector('.courses-item')), memoUl: m && r(m.querySelector('ul.items')), memoHandle: m && r(m.querySelector('.courses-item .drag-handle')) }; }"""
    async def prepare(page):
        await js(page, """() => { addCategory('Maison'); const a = DATA[DATA.length - 1]; addQuickTask(a, 'Trier la cave'); addQuickTask(a, 'Ampoule');
            addCategory('Bureau'); const b = DATA[DATA.length - 1]; addQuickTask(b, 'Agrafes');
            addCategory('Épicerie'); const m = DATA[DATA.length - 1]; setCoursesList(m.id, true); renderAll(); addCoursesQuick(m, 'Pain\\nLait'); renderAll();
            setFolded(b.id, true); unfoldCat(a.id); unfoldCat(m.id); renderAll(); }""")
        await page.evaluate("() => { window.dispatchEvent(new Event('resize')); }"); await page.wait_for_timeout(900)
    await prepare(pg)
    o = await js(pg, pos)
    check(o["dx"] == 0 and o["ul"] == "0px", f"ordi : décalage appliqué ({o})")
    check(o["bulC"] is None or abs(o["bulC"] - o["chkC"]) < 0.6, f"ordi : points de l'urgent hors de la colonne des cases ({o})")
    ctx, tel, errs = await _tel(pg)
    try:
        await prepare(tel)
        t = await js(tel, pos)
        check(t["dx"] == 20, f"téléphone : --ph-dx vaut {t['dx']}")
        check(abs(t["field"] - t["dx"] - t["chk"]) < 1.5, f"téléphone : le champ fermé a bougé ou les cases n'ont pas glissé ({t})")
        check(t["memoLi"] is not None and abs(t["memoLi"] - t["memoUl"] - t["dx"]) < 1.5, f"mémo : le filet part du bord ({t})")
        check(t["memoHandle"] is not None and t["memoHandle"] < t["memoLi"], f"mémo : la poignée n'a pas glissé ({t})")
        check(abs(t["ordC"] - t["chkC"]) < 0.6 and abs(t["mordC"] - t["dotC"]) < 0.6, f"flèche de tri pas centrée sur les cases / ronds ({t})")
        check(t["bulC"] is None or abs(t["bulC"] - t["chkC"]) < 0.6, f"téléphone : points de l'urgent hors de la colonne des cases ({t})")
        check(not errs, "erreur JavaScript au téléphone : " + "; ".join(errs[:3]))
    finally:
        await ctx.close()

async def t_signets(pg):
    """11.23 : la pile des signets suit l'ordre des cases, distingue listes et mémos, et mène à la bonne case."""
    a = await new_list(pg, "Maison"); await add_tasks(pg, a, "Porte", "Volet")
    m = await new_list(pg, "Courses", memo=True)
    for i in range(6): await new_list(pg, f"Liste {i}")
    z = await new_list(pg, "Tout en bas"); await add_tasks(pg, z, "Une")
    shots = os.environ.get("CAPTURES")
    await pg.click(".sig-tab"); await pg.wait_for_timeout(300)
    if shots: await pg.screenshot(path=f"{shots}/ordi-pile.png")
    ids = await js(pg, "() => [...document.querySelectorAll('.sig')].map(b => b.dataset.id)")
    ordre = await js(pg, "() => [...document.querySelectorAll('#categories > [id^=cat-]')].map(n => n.id.slice(4))")
    check(ids == ordre, "les signets ne suivent pas l'ordre des cases")
    check(await js(pg, f"() => document.querySelector('.sig[data-id=\"{m}\"]').classList.contains('sig-memo')"), "le mémo n'a pas son signet de mémo")
    check(await js(pg, f"() => document.querySelector('.sig[data-id=\"{a}\"] .sig-count').textContent") == "2", "bulle fausse")
    await pg.click(f".sig[data-id='{z}']"); await pg.wait_for_timeout(1200)
    check(not await js(pg, "document.getElementById('signets').classList.contains('open')"), "la pile reste ouverte")
    top = await js(pg, f"document.getElementById('cat-{z}').getBoundingClientRect().top")
    check(-2 < top < 80, f"la case n'est pas en haut de l'écran ({top})")
    check(await js(pg, f"document.getElementById('cat-{z}').classList.contains('sig-flash')"), "la case n'est pas cernée")
    if shots: await pg.screenshot(path=f"{shots}/ordi-arrivee.png")
    # l'onglet reste visible en bas de page
    vis = await js(pg, "(() => { const r = document.querySelector('.sig-tab').getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight && r.right <= innerWidth; })()")
    check(vis, "l'onglet n'est plus à l'écran après le défilement")
    # clic ailleurs : se referme
    await pg.click(".sig-tab"); await pg.mouse.click(20, 400); await pg.wait_for_timeout(200)
    check(not await js(pg, "document.getElementById('signets').classList.contains('open')"), "un clic ailleurs ne referme pas la pile")
    # survol (ordi) : la pile s'ouvre, et se referme quand on la quitte
    await pg.mouse.move(5, 5); await pg.wait_for_timeout(300)
    t = await pg.locator(".sig-tab").bounding_box()
    await pg.mouse.move(t["x"] + 15, t["y"] + 15, steps=3); await pg.wait_for_timeout(400)
    check(await js(pg, "document.getElementById('signets').classList.contains('open')"), "le survol n'ouvre pas la pile")
    await pg.mouse.move(5, 300, steps=3); await pg.wait_for_timeout(600)
    check(not await js(pg, "document.getElementById('signets').classList.contains('open')"), "ouverte au survol, la pile ne se referme pas quand on la quitte")
    # ouverte d'un clic : on la quitte et on fait défiler, elle reste ; un clic ailleurs la ferme
    await pg.click(".sig-tab"); await pg.mouse.move(5, 300, steps=3); await pg.mouse.wheel(0, 400); await pg.wait_for_timeout(700)
    check(await js(pg, "document.getElementById('signets').classList.contains('open')"), "ouverte d'un clic, la pile se ferme en défilant")
    await pg.mouse.click(20, 400); await pg.wait_for_timeout(200)
    check(not await js(pg, "document.getElementById('signets').classList.contains('open')"), "un clic ailleurs ne ferme pas la pile ouverte d'un clic")
    await js(pg, "window.scrollTo(0, 0)")
    # case fermée : entrouverte par le signet, pas punaisée ; elle attend qu'on y passe, puis se referme en la quittant
    await js(pg, "() => { DATA.forEach(y => setFolded(y.id, true)); renderAll(); }"); await pg.wait_for_timeout(300)
    await pg.click(".sig-tab"); await pg.wait_for_timeout(300)
    await pg.click(f".sig[data-id='{a}']"); await pg.wait_for_timeout(900)
    peek = f"document.getElementById('cat-{a}').classList.contains('peek')"
    check(await js(pg, peek), "le signet n'entrouvre pas la case fermée")
    check(await js(pg, f"isFolded('{a}')"), "le signet a punaisé la case")
    await pg.mouse.move(1250, 850, steps=6); await pg.wait_for_timeout(700)
    check(await js(pg, peek), "la case se referme avant qu'on y passe")
    b = await pg.locator(f"#cat-{a}").bounding_box()
    await pg.mouse.move(b["x"] + b["width"] / 2, b["y"] + 20, steps=5); await pg.wait_for_timeout(500)
    await pg.mouse.move(1250, 850, steps=5); await pg.wait_for_timeout(900)
    check(not await js(pg, peek), "survolée puis quittée, la case reste entrouverte")
    # duel : le nom de l'adversaire (11.24) ; simulé : le mode hors ligne n'a ni partage ni duel partagé
    nom = await js(pg, f"""() => {{ const d = '{z}', oD = isDuelList, oP = listPeople, oN = personName;
        isDuelList = id => id === d; listPeople = id => id === d ? ['u1'] : []; personName = u => u === 'u1' ? 'Hiske' : '?';
        Signets.open(); const t = document.querySelector('.sig[data-id="' + d + '"] .sig-title').textContent;
        Signets.close(); isDuelList = oD; listPeople = oP; personName = oN; return t; }}""")
    check(nom == "Duel avec Hiske", f"signet du duel : {nom}")
    # téléphone
    ctx = await pg.context.browser.new_context(viewport={"width": 390, "height": 760}, has_touch=True, is_mobile=True, device_scale_factor=2)
    tel = await ctx.new_page()
    await tel.goto(pg.url); await tel.wait_for_timeout(1200)
    for i in range(10): c = await new_list(tel, f"Liste {i}", memo=(i == 2)); await add_tasks(tel, c, "Une", "Deux")
    r = await js(tel, "(() => { const r = document.querySelector('.sig-tab').getBoundingClientRect(); return [r.right, r.width, r.height, innerWidth]; })()")
    check(abs(r[0] - r[3]) < 1.5 and r[2] >= 44, f"onglet du téléphone mal placé {r}")
    top = await js(tel, "document.querySelector('.sig-tab').getBoundingClientRect().top")
    check(top < 40, f"au téléphone, l'onglet n'est pas en haut de l'écran en haut de page ({top})")
    gap = await js(tel, "(() => { const t = document.querySelector('.sig-tab').getBoundingClientRect(); return Math.min(...[...document.querySelectorAll('.cat-full svg')].map(f => f.getBoundingClientRect().right > 0 ? t.left - f.getBoundingClientRect().right : 99)); })()")
    check(gap >= 0, f"au téléphone, l'onglet recouvre la flèche pleine page ({gap})")
    if shots: await tel.screenshot(path=f"{shots}/tel-ferme.png")
    await tel.tap(".sig-tab"); await tel.wait_for_timeout(300)
    if shots: await tel.screenshot(path=f"{shots}/tel-pile.png")
    h = await js(tel, "Math.min(...[...document.querySelectorAll('.sig')].map(b => b.getBoundingClientRect().height))")
    check(h >= 44, "signets trop petits au doigt")
    sw = await js(tel, "document.documentElement.scrollWidth <= innerWidth")
    check(sw, "la pile fait déborder la page de côté")
    # faire défiler derrière au doigt (appui sans toucher franc) : la pile reste ; un toucher ailleurs la ferme
    await js(tel, "() => { document.querySelector('.progress-card').dispatchEvent(new PointerEvent('pointerdown', { bubbles:true, pointerType:'touch' })); window.scrollBy(0, 300); }")
    await tel.wait_for_timeout(300)
    check(await js(tel, "document.getElementById('signets').classList.contains('open')"), "au doigt, faire défiler ferme la pile")
    await tel.tap("footer"); await tel.wait_for_timeout(300)
    check(not await js(tel, "document.getElementById('signets').classList.contains('open')"), "au doigt, toucher ailleurs ne ferme pas la pile")
    await ctx.close()

# --- lancement --------------------------------------------------------------
async def main():
    args = [a for a in sys.argv[1:] if a != "complet"]
    page = args[0] if args else "essai.html"
    url = (ROOT / page).as_uri()
    tests = [(n, f) for n, f in globals().items() if n.startswith("t_") and callable(f) and (not __import__("os").environ.get("SEUL") or __import__("os").environ["SEUL"] in n)]
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
    tout = ok == len(tests)
    if "complet" in sys.argv[1:]:
        # chantier de la 11 : le banc doit se comporter exactement comme l'appli publiée
        import subprocess
        print("\ncomparateur jumeaux (index.html ↔ essai.html)…", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "tests" / "jumeaux.py")], env=dict(os.environ, COURT="1"))
        tout = tout and r.returncode == 0
    sys.exit(0 if tout else 1)

asyncio.run(main())
