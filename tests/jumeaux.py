#!/usr/bin/env python3
"""Comparateur « jumeaux » (chantier de la 11).

Rejoue exactement les mêmes gestes sur deux fichiers — par défaut index.html
(la référence publiée) et essai.html (le banc) — et exige, après CHAQUE geste :
  - le même contenu du stockage (toutes les fiches, la corbeille, etc.) ;
  - le même écran (la page entière, attributs compris, hors numéro de version
    et dessin du jeu).
Hasard et date sont figés à l'identique des deux côtés.

    python3 tests/jumeaux.py                      # données d'exemple (tests/donnees-exemple.json)
    DONNEES=/chemin/sauvegarde.json python3 tests/jumeaux.py   # une vraie sauvegarde, hors ligne
    python3 tests/jumeaux.py index.html index.html            # contrôle : un fichier contre lui-même

Rien n'est envoyé nulle part : Firebase est bloqué, chaque côté a son profil jetable.
"""
import asyncio, os, sys, pathlib, json, difflib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
DONNEES = os.environ.get("DONNEES", str(ROOT / "tests" / "donnees-exemple.json"))
FIXED_NOW = "2026-11-13T10:00:00+01:00"   # un vendredi
VUES = [("ordinateur", {"width": 1300, "height": 900}), ("téléphone", {"width": 390, "height": 844})]
if os.environ.get("VUE"): VUES = [v for v in VUES if v[0].startswith(os.environ["VUE"])]
SETTLE = int(os.environ.get("SETTLE", "500"))   # ms d'attente après un geste (animations)

# Hasard rejouable, identique des deux côtés
INIT = r"""(() => {
  // Hasard rejouable. Une suite PAR CHAÎNE D'APPEL (noms des fonctions qui tirent,
  // pas les numéros de ligne : ils bougent d'un fichier à l'autre) : un tirage
  // décoratif de plus (animation, confettis) ne décale pas ceux qui comptent
  // (phrases, trèfle, identifiants des tâches).
  const site = () => new Error().stack.split("\n").slice(3, 7).map(l => (l.match(/at (?:async )?([^\s(]+) \(/) || [0, "?"])[1]).join(">");
  const suite = seeds => () => {
    const k = site(); let s = seeds.get(k);
    if(s === undefined){ s = 7; for(const ch of k) s = (s * 31 + ch.charCodeAt(0)) % 2147483648; }
    s = (s * 1103515245 + 12345) % 2147483648; seeds.set(k, s); return s;
  };
  const r1 = suite(new Map()), r2 = suite(new Map());
  Math.random = () => r1() / 2147483648;
  crypto.getRandomValues = a => { for(let i = 0; i < a.length; i++) a[i] = r2() >> 16; return a; };
})();"""

SNAP = r"""() => {
  const store = {};
  for(let i = 0; i < localStorage.length; i++){
    const k = localStorage.key(i);
    if(/sltapis:rev$/.test(k)) continue;              // compteur d'écritures
    store[k] = localStorage.getItem(k);
  }
  const clone = document.body.cloneNode(true);
  clone.querySelectorAll(".version-tag").forEach(e => e.textContent = "");
  clone.querySelectorAll("script, style").forEach(e => e.remove());   // le code lui-même n'est pas « l'écran »
  // dessins (jeu, tapis) : taille du canevas recalculée en différé → ignorée ;
  // petit message (toast) : on garde son texte, pas l'instant où il s'efface
  clone.querySelectorAll("canvas").forEach(e => { e.removeAttribute("width"); e.removeAttribute("height"); e.removeAttribute("style"); });
  clone.querySelectorAll("#toast").forEach(e => e.classList.remove("show"));
  clone.querySelectorAll(".tapis-box").forEach(e => e.removeAttribute("style"));   // décor du fond, recalé en différé
  const etat = { y: Math.round(scrollY), actif: document.activeElement ? (document.activeElement.className || document.activeElement.tagName) : "",
    defil: [...document.querySelectorAll("ul.items, .chat-log")].map(u => Math.round(u.scrollTop)).join(",") };
  return { store, dom: clone.outerHTML, etat };
}"""

LOAD = """d => { d = JSON.parse(d);
  // « moi » = le compte qui possède le plus de listes : les règles du partage (invité,
  // initiales, qui efface quoi) jouent comme en vrai, sans connexion
  const n = {}; d.lists.forEach(L => { if(L.owner) n[L.owner] = (n[L.owner] || 0) + 1; });
  const moi = Object.keys(n).sort((a, b) => n[b] - n[a])[0];
  if(moi) localStorage.setItem(Store.ns + "me", moi);
  Store.importModel(d); DATA.length = 0; reloadAllFromStorage(); renderAll(); }"""

# ---------------------------------------------------------------------------
# Gestes. Chaque geste : (nom, fonction async pg). Sélecteurs ou appels du
# code de l'appli, identiques pour les deux fichiers. pg.autre = un 2e onglet
# du même navigateur (même stockage) : ce qu'il écrit arrive au 1er onglet
# par le vrai chemin « autre onglet » (celui qu'emprunte aussi la synchro).
async def ev(pg, code, arg=None): return await pg.evaluate(code, arg)

LISTE = ".category:not(.courses):not(.collapsed)"
MEMO = ".category.courses:not(.collapsed)"
TACHE = LISTE + " .item:not(.is-checked):not(.is-egg):not(.add-form-row)"

async def centrer(loc):
    await loc.evaluate("e => e.scrollIntoView({ block: 'center', inline: 'nearest' })")
def clic(sel, i=0, dbl=False, centre=True):
    async def f(pg):
        loc = pg.locator(sel).nth(i)
        await loc.wait_for(state="attached")
        if not centre:                  # petite fenêtre : clic direct, sans faire défiler la page (ça la refermerait)
            await loc.dispatch_event("click"); return
        await centrer(loc)
        if not await loc.is_visible():          # bouton qui n'apparaît qu'au survol
            await loc.dispatch_event("click"); return
        if dbl: await loc.dblclick()
        else: await loc.click(force=True)
    return f
def taper(sel, texte, entree=True, i=0):
    async def f(pg):
        loc = pg.locator(sel).nth(i)
        await loc.click(force=True); await loc.fill(""); await loc.type(texte)
        if entree: await pg.keyboard.press("Enter")
    return f
def touche(k): return lambda pg: pg.keyboard.press(k)
def suite(*fs):
    async def f(pg):
        for x in fs: await x(pg); await pg.wait_for_timeout(250)
    return f
def glisser(src, dst, i=0, j=1):
    async def f(pg):
        a, b = pg.locator(src).nth(i), pg.locator(dst).nth(j)
        await centrer(a)
        ba, bb = await a.bounding_box(), await b.bounding_box()
        await pg.mouse.move(ba["x"] + ba["width"] / 2, ba["y"] + ba["height"] / 2); await pg.mouse.down()
        for k in range(1, 13):
            await pg.mouse.move(ba["x"] + ba["width"] / 2 + (bb["x"] - ba["x"]) * k / 12, ba["y"] + ba["height"] / 2 + (bb["y"] + bb["height"] * .7 - ba["y"] - ba["height"] / 2) * k / 12)
            await pg.wait_for_timeout(30)
        await pg.mouse.up()
        # le défilement automatique pendant un glisser dépend du temps écoulé : on repart du haut
        await pg.wait_for_timeout(500); await pg.evaluate("() => scrollTo(0, 0)")
    return f
def ailleurs(code):
    """Le 2e onglet fait un geste (code JS de l'appli) ; le 1er le reçoit."""
    async def f(pg):
        # ouvert le temps du geste seulement : deux onglets ouverts en permanence se
        # marchent parfois dessus (bug connu de la 10.81 : +1 d'« En cours » annulé)
        autre = await pg.context.new_page()
        await autre.clock.set_fixed_time(FIXED_NOW)
        await autre.route("**/*gstatic.com/**", lambda r: r.abort())
        await autre.goto((ROOT / pg.fichier).as_uri()); await autre.wait_for_timeout(900)
        await autre.evaluate(code); await autre.wait_for_timeout(700)
        await autre.close(); await pg.bring_to_front()
    return f
def distant(choix, modif):
    """L'autre personne d'une liste partagée la modifie « en ligne ». choix : quelle liste
    (JS, reçoit la fiche L et mon compte) ; modif : ce qu'elle change (JS, reçoit L et son compte)."""
    code = """() => { const docs = Store.readDocs(), moi = Store.myUid();
      const L = Object.values(docs.lists).sort((a, b) => a.id < b.id ? -1 : 1).find(L => !L.deleted && (L.members || []).length > 1 && (%s));
      const elle = (L.members || []).find(m => m !== moi);
      (%s)(L, elle);
      Store.writeDocs({ lists: { [L.id]: L } });
      storeChangedElsewhere(Store.ns + "remote-shared"); }""" % (choix, modif)
    return lambda pg: pg.evaluate(code)
NORMALE = "!L.type && L.owner === moi"
AJOUT = lambda titre, ident: "(L, elle) => { L.items.push({ id: '%s', base: { t: '%s', by: elle, at: Date.now() } }); if(Array.isArray(L.order)) L.order.push('%s'); }" % (ident, titre, ident)
COCHE = "(L, elle) => { const it = L.items.find(i => !i.done && !(i.edits && (i.edits.deleted || i.edits.waiting))); it.done = true; it.checkedAt = new Date().toISOString(); it.edits = Object.assign(it.edits || {}, { doneBy: elle }); }"
async def coller(pg):
    loc = pg.locator(LISTE + " .cat-quick").first
    await centrer(loc); await loc.click(force=True)
    await loc.evaluate("e => { const dt = new DataTransfer(); dt.setData('text/plain', 'Ligne une\\nLigne deux\\n- Ligne trois'); e.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true })); }")

def convertir(sel):
    """Double-clic sur le titre puis « Convertir » ; sel=None : la même case que la fois d'avant."""
    async def f(pg):
        if sel: pg.converti = await pg.locator(sel).first.get_attribute("id")
        card = "#" + pg.converti
        await clic(card + " .cat-title", 0, dbl=True)(pg); await pg.wait_for_timeout(250)
        await clic(card + " .cat-convert:not(.cat-copy) button")(pg)
    return f

async def survol_hors(pg): await pg.mouse.move(2, 2)
async def survol(pg):
    loc = pg.locator(".category.collapsed").first
    await centrer(loc); bb = await loc.bounding_box()
    await pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + 20); await pg.wait_for_timeout(200)
    await pg.mouse.move(bb["x"] + bb["width"] / 2 + 3, bb["y"] + 24)

UNE_LISTE = "DATA.find(x => !isSideList(x.id) && !isCategoryDeleted(x.id) && iOwnList(x.id))"

GESTES = [
    ("rendu de départ", lambda pg: ev(pg, "() => renderAll()")),
    # tâches
    ("cocher une tâche", clic(TACHE + " .check, " + TACHE + " input[type=checkbox]")),
    ("décocher la même", clic(LISTE + " .item.is-checked .check, " + LISTE + " .item.is-checked input[type=checkbox]")),
    ("ajout express (saisie sous le titre)", taper(LISTE + " .cat-quick", "Acheter des ampoules")),
    ("ajout par le +", suite(clic(LISTE + " .cat-head-right .add-btn"), taper(".add-form-row .add-title", "Tâche du plus", entree=False), clic(".add-form-row .add-save"))),
    ("+ puis Échap", suite(clic(LISTE + " .cat-head-right .add-btn", 1), touche("Escape"))),
    ("modifier une tâche (double-clic, Enregistrer)", suite(clic(TACHE + " .item-title", 0, dbl=True), taper(".item.editing .edit-title", "Titre modifié", entree=False), clic(".item.editing .edit-save"))),
    ("modifier puis Échap", suite(clic(TACHE + " .item-title", 1, dbl=True), touche("Escape")), 1500),
    ("annuler (⌘Z)", touche("Control+z")),
    ("refaire un ⌘Z", touche("Control+z")),
    ("inverser le sens d'une liste", clic(LISTE + " .cat-order")),
    ("effacer une tâche", clic(TACHE + " .delete-btn")),
    ("glisser une tâche dans sa liste", glisser(TACHE + " .drag-handle", TACHE, 0, 2)),
    ("glisser une tâche vers une autre liste (ordi)", lambda pg: glisser(TACHE + " .drag-handle", ".category:not(.courses):not(.collapsed) .cat-head", 0, 1)(pg) if pg.viewport_size["width"] > 600 else ev(pg, "() => 0")),
    ("glisser une liste (ordi)", lambda pg: glisser(".category .cat-grip", ".category", 0, 1)(pg) if pg.viewport_size["width"] > 600 else ev(pg, "() => 0")),
    ("prendre une tâche et la reposer à sa place", glisser(TACHE + " .drag-handle", TACHE, 0, 0)),
    ("prendre une liste et la reposer à sa place (ordi)", lambda pg: glisser(".category .cat-grip", ".category .cat-head", 0, 0)(pg) if pg.viewport_size["width"] > 600 else ev(pg, "() => 0")),
    ("cocher juste après", clic(TACHE + " input[type=checkbox]", 1)),
    # mémos
    ("rayer un article de mémo", clic(MEMO + " .courses-item .item-text")),
    ("dé-rayer", clic(MEMO + " .courses-item.is-checked .item-text")),
    ("ajouter un article", taper(MEMO + " .courses-input", "2 moutarde")),
    ("modifier un article (détail)", suite(clic(MEMO + " .courses-item:not(.editing) .item-text", 0, dbl=True), taper(".courses-edit-note", "bio", entree=True))),
    ("vider les rayés", clic(MEMO + " .courses-clear")),
    # urgent, en cours, trèfle
    ("triangle urgent (retirer)", clic("#urgentBanner .urgent-list li .urgent-btn")),
    ("case urgente → en cours", clic("#urgentBanner .urgent-list li .waiting-btn")),
    ("fenêtre de relance : premier choix", clic(".relance-pop .rp-chip", centre=False), 2500),
    ("en cours → retour dans sa liste", clic("#waitingList .waiting-btn")),
    ("trèfle : ouvrir", clic("#luckyLine")),
    ("trèfle : choisir", clic("#luckyLine .lucky-pick")),
    ("envoyer en cours (appel direct)", lambda pg: ev(pg, "() => { const c = " + UNE_LISTE + "; const i = getEffectiveItems(c).findIndex((b, i) => !isDeleted(itemKey(c.id, i))); sendToWaiting(itemKey(c.id, i), ''); }")),
    # cases
    ("pleine page", clic(LISTE + " .cat-full")),
    ("sortir de la pleine page", clic(".fp-back")),
    ("retirer la punaise (fermer une case)", clic(".category:not(.collapsed) .cat-fold", 1)),
    ("survoler une case fermée", survol),
    ("planter la punaise d'une case fermée", clic(".category.collapsed .cat-fold")),
    ("souris ailleurs", survol_hors),
    ("renommer une liste + couleur", suite(clic(LISTE + " .cat-title", 2, dbl=True), taper(".cat-title-input", "Nouveau nom", entree=False), clic(".cat-swatch", 3), clic(".cat-edit-actions .edit-save"))),
    ("nouvelle liste", suite(clic(".add-category-btn"), taper(".nl-name", "Liste neuve", entree=False), clic(".nl-save"))),
    ("supprimer la case vide", clic(".category.can-delete .cat-delete-btn")),
    # écrans
    ("chat : écrire un message", suite(clic(".chat-screen"), lambda pg: pg.keyboard.type("salut les jumeaux"), touche("Enter"))),
    ("duel : lancer", clic(".d-lancer"), 6000),
    # panneaux
    ("corbeille : ouvrir", clic("#trashLink")),
    ("corbeille : fermer", clic(".trash-close")),
    ("coller plusieurs lignes", coller),
    ("partage : ouvrir le panneau", clic("#shareLink")),
    ("partage : fermer (Échap)", touche("Escape")),
    ("convertir une liste (non partagée) en mémo", convertir(".category:not(.courses):not(.collapsed):not(.has-people)")),
    ("la reconvertir en liste", convertir(None)),
    # l'autre personne (listes partagées), par le chemin de la synchro
    ("elle ajoute une tâche à une liste partagée", distant(NORMALE, AJOUT("Ajoutée par elle", "tdistant00001"))),
    ("je coche la 1re tâche de cette liste juste après", clic(".category.has-people:not(.courses):not(.collapsed) .item:not(.is-checked):not(.is-egg) input[type=checkbox]")),
    ("elle coche une tâche", distant(NORMALE, COCHE)),
    ("j'efface une tâche de cette liste juste après", clic(".category.has-people:not(.courses):not(.collapsed) .item .delete-btn")),
    ("elle raye un article d'un mémo partagé", distant("L.type === 'courses'", "(L, elle) => { const it = L.items.find(i => !i.done && !(i.edits && i.edits.deleted)); it.done = true; it.edits = Object.assign(it.edits || {}, { doneBy: elle }); }")),
    ("je raye un autre article juste après", clic(".category.courses.has-people:not(.collapsed) .courses-item:not(.is-checked) .item-text")),
    ("elle écrit dans le chat", distant("L.type === 'chat'", "(L, elle) => { L.items.push({ id: 'tdistant00002', base: { t: 'coucou de l’autre côté', by: elle, at: Date.now() } }); }")),
    ("je réponds dans le chat", suite(clic(".chat-screen"), lambda pg: pg.keyboard.type("bien reçu"), touche("Enter"))),
    ("elle ajoute pendant que je modifie une tâche", suite(clic(TACHE + " .item-title", 0, dbl=True), distant(NORMALE, AJOUT("Arrivée pendant ma modif", "tdistant00003")))),
    ("j'enregistre ma modification", suite(taper(".item.editing .edit-title", "Modifiée pendant son ajout", entree=False), clic(".item.editing .edit-save")), 800),
    ("elle ajoute pendant qu'une liste est en pleine page", suite(clic(LISTE + " .cat-full"), distant(NORMALE, AJOUT("Arrivée en pleine page", "tdistant00004")))),
    ("je sors de la pleine page", clic(".fp-back")),
    ("elle renomme sa liste (dont je suis l'invité)", distant("L.owner !== moi", "(L, elle) => { L.title = 'Renommée par elle'; }")),
    ("⌘Z après un changement venu d'elle (ne doit rien défaire d'elle)", touche("Control+z")),
    ("elle ne me partage plus sa liste", lambda pg: pg.evaluate("""() => { const docs = Store.readDocs(), moi = Store.myUid();
        const L = Object.values(docs.lists).sort((a, b) => a.id < b.id ? -1 : 1).find(L => !L.deleted && L.owner && L.owner !== moi);
        Store.writeDocs({ lists: { [L.id]: null } }); storeChangedElsewhere(Store.ns + "remote-shared"); }""")),
    # d'ailleurs (autre onglet)
    ("autre onglet : ajoute une tâche", ailleurs("() => { addQuickTask(" + UNE_LISTE + ", 'Venue d’ailleurs'); renderAll(); }")),
    ("autre onglet : coche une tâche", ailleurs("() => { const c = " + UNE_LISTE + "; const i = getEffectiveItems(c).findIndex((b, i) => !isDeleted(itemKey(c.id, i)) && !state[itemKey(c.id, i)]); setDone(itemKey(c.id, i), true); renderAll(); }")),
    ("autre onglet : efface une tâche", ailleurs("() => { document.querySelector('.category:not(.courses) .item .delete-btn').click(); }")),
    ("⌘Z après un changement venu d'ailleurs", touche("Control+z")),
    ("tourner le téléphone / changer la fenêtre", lambda pg: pg.set_viewport_size({"width": pg.viewport_size["height"], "height": pg.viewport_size["width"]})),
    ("revenir", lambda pg: pg.set_viewport_size({"width": pg.viewport_size["height"], "height": pg.viewport_size["width"]})),
]

# ---------------------------------------------------------------------------
async def open_side(browser, page, dump, vp):
    ctx = await browser.new_context(viewport=vp, has_touch=vp["width"] < 600)
    await ctx.add_init_script(INIT)
    pg = await ctx.new_page()
    pg.set_default_timeout(4000)
    await pg.clock.set_fixed_time(FIXED_NOW)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.route("**/*gstatic.com/**", lambda r: r.abort())
    await pg.goto((ROOT / page).as_uri()); await pg.wait_for_timeout(1200)
    await pg.evaluate(LOAD, dump); await pg.wait_for_timeout(SETTLE)
    pg.autre = None; pg.fichier = page
    return ctx, pg, errs

if os.environ.get("JUSQUA"):   # pour chercher : s'arrêter après le geste dont le nom commence ainsi
    GESTES = GESTES[:next(i for i, g in enumerate(GESTES) if g[0].startswith(os.environ["JUSQUA"])) + 1]

def first_diff(a, b, label):
    al, bl = a.replace(">", ">\n").splitlines(), b.replace(">", ">\n").splitlines()
    d = list(difflib.unified_diff(al, bl, "référence", "banc", n=1, lineterm=""))
    return f"{label} diffère :\n    " + "\n    ".join(x[:220] for x in d[:14])

async def jouer(p, page, dump, vp):
    """Joue toute la séquence sur un fichier, seul dans son navigateur ; rend un relevé par geste."""
    browser = await p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx, pg, errs = await open_side(browser, page, dump, vp)
    out = []
    for g in GESTES:
        name, geste, extra = (g + (0,))[:3]
        rate = None
        try: await geste(pg)
        except Exception as e: rate = str(e).splitlines()[0]
        # on attend que l'écran ne bouge plus (animations, compteur) : deux relevés
        # identiques à 350 ms d'écart, 10 s au plus
        await pg.wait_for_timeout(SETTLE + extra)
        snap = await pg.evaluate(SNAP)
        for _ in range(26):
            await pg.wait_for_timeout(350)
            again = await pg.evaluate(SNAP)
            if again == snap: break
            snap = again
        snap["rate"] = rate; snap["errs"] = errs[:]; errs.clear()
        out.append(snap)
    await browser.close()
    return out

def comparer(name, sa, sb):
    norm = lambda st: {k.split("essai:", 1)[-1]: v for k, v in st.items()}   # « essai: » : préfixe du banc
    res = []
    if sa["rate"] or sb["rate"]: res.append(f"geste impossible : {sa['rate']} / {sb['rate']}")
    pa, pb = norm(sa["store"]), norm(sb["store"])
    if pa != pb:
        bad = [k for k in sorted(set(pa) | set(pb)) if pa.get(k) != pb.get(k)]
        res.append("stockage diffère : " + ", ".join(bad[:5]))
        x, y = pa.get(bad[0]) or "", pb.get(bad[0]) or ""
        k = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
        res.append(f"  {bad[0]} : …{x[max(0,k-80):k+80]}…\n      ≠ …{y[max(0,k-80):k+80]}…")
    if sa["dom"] != sb["dom"]: res.append(first_diff(sa["dom"], sb["dom"], "écran"))
    if sa["etat"] != sb["etat"]: res.append(f"défilement / champ actif : {sa['etat']} ≠ {sb['etat']}")
    if sa["errs"] or sb["errs"]: res.append("erreur JavaScript : " + "; ".join((sa["errs"] + sb["errs"])[:3]))
    return res

async def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    banc = sys.argv[2] if len(sys.argv) > 2 else "essai.html"
    dump = open(DONNEES).read()
    print(f"jumeaux : {ref} ↔ {banc} — données : {pathlib.Path(DONNEES).name}", flush=True)
    ok = True; total = 0
    async with async_playwright() as p:
        # un navigateur à la fois (sur une machine à 2 cœurs, deux en parallèle finissent par planter) ;
        # PARALLELE=1 pour en lancer deux à la fois sur une machine plus costaude
        rs = []
        for _, vp in VUES:
            if os.environ.get("PARALLELE"): rs += await asyncio.gather(jouer(p, ref, dump, vp), jouer(p, banc, dump, vp))
            else: rs += [await jouer(p, ref, dump, vp), await jouer(p, banc, dump, vp)]
        for n, (vname, vp) in enumerate(VUES):
            print(f"— {vname}")
            for g, sa, sb in zip(GESTES, rs[2 * n], rs[2 * n + 1]):
                res = comparer(g[0], sa, sb); total += 1
                if res:
                    ok = False; print(f"  ÉCART   {g[0]}"); [print("    " + r) for r in res]
                elif not os.environ.get("COURT"):
                    print(f"  ok      {g[0]}")
    print(f"\njumeaux : {total} contrôles — " + ("identiques ✔" if ok else "ÉCARTS ✘"))
    return ok

if __name__ == "__main__":
    sys.exit(0 if asyncio.run(main()) else 1)
