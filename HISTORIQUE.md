# Sous le tapis — historique des versions

Sorti du fichier de l'appli en 10.74 (grand ménage) pour l'alléger ; rien n'est perdu.
Les entrées sont dans l'ordre où elles avaient été écrites (pas toujours chronologique).

  - 10.74 : grand ménage, sans changement à l'écran : anciennes versions dans archives/,
    historique sorti vers ce fichier, 15 règles CSS en double fusionnées ; synchro : une salve
    de listes arrivées d'un coup (ouverture) ne donne plus qu'un seul rendu au lieu d'un par liste.
```
  - 5.2 : case trèfle « Une petite sur le pouce ? » sous les urgences —
    deux tâches tirées au sort chaque jour (plutôt les anciennes), clic =
    choix (liseré jaune + case à cocher), clic dans le fond = annuler,
    case grisée « Trèfle du jour fait ! » une fois cochée.
  - 5.3 : bouton de départ blanc / survol vert pâle ; section « En cours »
    masquée tant qu'aucune liste n'existe.
  - 5.4 : bouton ⟳ pour un nouveau tirage du trèfle ; dans la case urgente,
    au survol, ↪ (envoyer en cours) et ⚠ (retirer l'urgence) à droite ;
    la purge du lundi vide aussi « En cours » (+ rattrapage unique).
  - 5.5 : infobulles sur ↪ / ⚠ de la case urgente et sur ⟳ ; au survol de
    ces icônes, plus de carré de fond, l'icône se renforce simplement.
  - 5.6 : pas d'infobulle sur ⟳ (elle tournait avec l'icône) ; l'icône suffit.
  - 5.7 : triangle « urgent » en bas à droite des formulaires de création
    et de modification d'une tâche.
  - 5.8 : Ajouter / Enregistrer blancs, verts au survol (Annuler : gris) ; triangle du
    formulaire avec le petit carré gris arrondi au survol (comme ailleurs).
  - 5.9 : une nouvelle tâche urgente arrive bien en tête de la case urgente
    (l'ordre de cette case est désormais enregistré).
  - 5.10 : une tâche qui arrive à l'échéance (veille, jour J, retard)
    remonte une fois en tête de la case urgente, même si elle y était déjà.
  - 5.11 : seuil d'urgence par l'échéance avancé à J-2 (DUE_URGENT_DAYS).
  - 5.12 : œuf « en couvaison » (champ egg) dans les formulaires, à côté du
    triangle (les deux s'excluent) : tâche grisée, en queue de liste, hors
    compteurs (sauf une fois cochée), hors trèfle et hors case urgente.
  - 5.13 : ligne d'un œuf : un point à la place de la case (on ne coche pas
    un œuf), plus de ↪, et à la place du ⚠ un œuf qui éclot (poussin) qui
    rend la tâche normale ; la croix reste.
  - 5.14 : le point est remplacé par l'œuf (grisé), plus d'œuf devant le titre.
  - 5.15 : œuf et œuf-poussin un peu plus grands.
  - 5.16 : trèfle complété s'il perd une proposition en cours de journée ;
    listes déplaçables par glisser-déposer (poignée ⠿ en haut à droite de
    chaque carte) à la place des flèches ▲▼.
  - 5.17 : glisser une liste : fantôme qui suit le pointeur, emplacement en
    pointillés qui s'aimante à la place la plus proche ; infobulle
    « Réorganiser » sur la poignée.
  - 5.18 : mouchetures sur l'œuf du formulaire ; titre « Une petite en
    douceur sur le pouce ? » ; « En cours » : envoyer en cours retire
    l'urgence, l'échéance n'y rend plus urgent, un marquage manuel donne
    juste l'aspect urgent + le haut de la case ; ordre de la case enregistré.
  - 5.19 : trèfle : titre droit, tâches en italique ; corbeille en police
    plus petite et sur deux colonnes (une seule sur téléphone).
  - 5.20 : envoyer en cours GARDE l'urgence manuelle (retour à l'ancien
    comportement, à la demande) : aspect urgent + haut de « En cours »,
    jamais dans la case urgente ; elle revient urgente dans sa liste.
  - 5.21 : « relance » : une tâche en cours avec une date (champ « Relance
    le ») revient le jour J dans la case urgente et dans le compteur, en
    bleu (--relance) ; ↩ dans la case urgente la sort d'« En cours ».
    État calculé (isRelance), aucune donnée modifiée.
  - 5.22 : tapis décoratif : clic sur le titre en haut à droite → un tapis
    d'Orient (coloris sauge) se déroule par-dessus l'appli, de la largeur des
    cases, du titre jusqu'au-dessus du numéro de version ; reclic sur le titre,
    clic sur le tapis ou Échap → il s'enroule. Purement décoratif : aucune
    donnée lue ni écrite (voir TAPIS et le bloc « tapis » en fin de script).
  - 5.23 : tapis : déroulé plus doux, à une vitesse qu'on voit à l'écran ;
    plus d'ombre autour du tapis ; franges droites et nettes ; petit son
    synthétisé (froissement de laine + « flop » feutré), sans fichier externe.
  - 5.24 : son du tapis plus doux et moins fort : souffle de tissu (bruit
    rose filtré, sans écrêtage ni grésillement), « flop » à peine marqué.
  - 6.0 : passage en version majeure à la demande d'André-Pierre (le tapis
    décoratif des 5.22–5.24 est en place). Aucun changement de code.
  - 6.1 : corbeille retravaillée : liste en plus petit, dans une fenêtre de
    hauteur fixe qui défile (en-têtes de jour collants) ; graphique des
    tâches accomplies au-dessus, avec un switch Jour / Semaine / Mois,
    comparaison avec la période précédente, record et série de jours.
    Calculé depuis les dates de coche existantes (corbeille + tâches
    cochées pas encore purgées) ; seule nouvelle clé : le choix du switch
    (« fauconnerie-v2-trashchart »). Aucune donnée existante modifiée.
  - 6.2 / 6.3 : refonte des couleurs, inspirée d'une feuille illustrée
    (aplats beurre, rose, bleu-gris) : bleu-vert + ardoise en principales,
    framboise poudrée (relances), ocre (douceur), bleu acier / menthe
    (« En cours »), rouge-orangé (urgent). Mode sombre ardoise froid.
    Fond en léger dégradé (frais en haut → crème en bas). Typo unifiée
    (4 tailles, plus d'italique ni de serif, titres en Plex Mono capitales).
    Cadres sans liseré (aplats) sauf le liseré gauche des listes. Compteur
    du haut : « x tâches réussies cette semaine » (repart chaque lundi),
    la barre garde faites / total. Gamme des listes renouvelée : les
    anciennes couleurs enregistrées sont AFFICHÉES dans la nouvelle gamme
    (displayCatColor), rien n'est réécrit. Boutons du bas en pastilles.
    Aucune clé de stockage ajoutée ni modifiée.
  - 7.0 : version majeure à la demande d'André-Pierre. Compteur « x tâches
    accomplies cette semaine » ; titre urgent plus gras (Plex Mono 700) ;
    bouton de relance de la case douceur dans l'ocre de son titre ; tapis
    recoloré dans la gamme fraîche (bleu-vert, ardoise, framboise, ocre,
    crème) au lieu du vert sapin / terracotta.
  - 7.1 : compteur « x tâches réussies ! » (toujours remis à zéro le lundi) ;
    à la place du compteur 2/5 d'une liste, un petit triangle ▲/▼ qui inverse
    l'ordre d'affichage (▲ par défaut : la plus récente en haut ; ▼ : en bas) —
    nouvelle clé « fauconnerie-v2-catreverse », rien d'autre réécrit ; tâches
    glissées avec fantôme et emplacement aimanté, y compris d'une liste à
    l'autre (la tâche est recopiée dans la nouvelle liste avec tous ses champs
    et sa coche, puis masquée dans l'ancienne, comme le changement de
    catégorie du formulaire) ; petit champ « Ajouter… » à côté du titre de
    chaque liste (Entrée = tâche ajoutée) ; tapis recoloré plus sobre
    (ardoise, bleu-gris, bronze éteint, plus de framboise) et un peu éteint.
  - 7.2 : le champ d'ajout express n'affiche plus « Ajouter… » mais un petit
    crayon discret (il s'efface quand on écrit) ; tâche urgente : seul le
    titre est en gras, plus le détail en dessous.
  - 7.3 : envoyer une tâche « en cours » ouvre un petit choix de relance
    (sans date, 1 semaine, 2 semaines, 1 mois, garder l'échéance si elle est
    à venir, ou date précise) : une échéance passée ne devient plus une
    relance immédiate. L'échéance d'origine est mise de côté (champ
    dueBeforeWaiting dans l'override) et revient quand la tâche rentre dans
    sa liste. Relance dans la case urgente : bouton « Reporter ». Bug du
    lundi : le compteur repartait à zéro à minuit mais la purge n'avait lieu
    qu'au rechargement — désormais la purge se fait au même moment, même
    onglet resté ouvert (vérification à chaque rendu et chaque minute).
  - 7.4 : accueil sans liste : « Go dépoussiérage » / « une petite liste ? ».
    (Rappel : la semaine bascule dimanche à minuit, soit lundi 00:00.)
  - 7.5 : fenêtre de relance « Un petit rappel de relance ? » aux couleurs
    d'« En cours », choix dans l'ordre 1 sem. / 2 sem. / 1 mois / pas de
    relance. Corbeille : regroupée par semaine (plus par jour), style
    archive neutre en police machine à écrire (Courier Prime), sans le nom
    de la liste, petite date à droite. Affichage seulement.
  - 7.6 : échéance et relance deviennent deux dates distinctes. Nouveau
    champ « relance » (override ou item). En cours : l'échéance est masquée
    (gardée intacte), seule la relance compte et s'affiche ; retour dans la
    liste : la relance est effacée, l'échéance réapparaît. Le formulaire
    d'une tâche en cours modifie la relance, pas l'échéance. Par défaut,
    aucune date de relance (champ date vide dans la fenêtre). Ancien format
    (≤ 7.5, la relance vivait dans « due ») : lu tel quel tant que la tâche
    n'a pas de champ « relance » ; dueBeforeWaiting y est repris comme
    échéance. Sauvegardes : « relance » exportée / importée.
  - 7.7 : en remettant dans sa liste une tâche qui avait une échéance, petite
    question : la garder, l'effacer ou choisir une nouvelle date (sans
    échéance, retour direct). Corbeille : « Semaine dernière ».
  - 7.8 : accueil sans liste aux couleurs de la case douceur (coquille d'œuf
    et ocre) et tapis en filigrane derrière (image décorative, effacée dès
    qu'une liste existe ; aucune donnée lue ni écrite).
  - 7.9 : le filigrane occupe exactement la place du tapis déroulé (du titre
    au numéro de version), plus visible ; bouton d'accueil blanc comme les
    propositions de la case douceur, « + » ocre, sous-titre au bleu du
    trèfle, halo jaune au survol.
  - 7.10 : accueil sans liste : Corbeille / Sauvegarder / Restaurer masqués
    (classe body.no-list) ; restaurer reste possible via un lien discret
    sous le bouton. Filigrane : de sous la case compteur jusqu'au bas de la
    fenêtre.
  - 7.11 : bouton d'accueil entouré de pointillés (le fantôme de la future
    liste) ; lien « restaurer » un peu plus grand et plus bas.
  - 7.12 : pointillés du bouton d'accueil en jaune ; au survol du lien, seul
    « restaurer une sauvegarde » est souligné (pas le « ou »).
  - 7.13 : champ « Un nom pour la liste ? » ; sur l'accueil sans liste, il
    s'affiche plus haut sur le tapis, liseré et boutons jaunes.
  - 7.14 : le champ glisse en douceur vers sa place (un peu moins haut) et son
    liseré passe du jaune au rose ; retour fluide si on annule.
  - 7.15 : le champ du nom prend exactement la place du bouton (centres
    alignés, ✓ et × à côté) ; à la création de la première liste, le tapis
    s'efface en fondu et le reste de la page apparaît en douceur.
  - 7.16 : case urgente visible dès qu'une liste existe, au calme quand elle
    est vide (« Rien d'urgent pour l'instant ») ; case douceur masquée tant
    qu'il y a moins de 3 tâches dans les listes, puis elle apparaît en
    fondu avec deux tâches tirées parmi elles (le tirage du jour fait avec
    moins de 3 tâches est oublié, sauf si une proposition a été cochée).
  - 7.17 : case urgente vide déjà dans son rouge ; « En cours » vide :
    « Rien pour l'instant. »
  - 7.18 : « Rien d'urgent pour l'instant » et « Rien pour l'instant » écrits
    en blanc, en léger relief (ombre de la couleur de leur case).
  - 7.19 : plus d'ombre : blanc pur, en gras.
  - 7.20 : « Rien pour l'instant » (En cours) repasse en gris très clair ;
    la case urgente vide garde son blanc.
  - 7.21 : « En cours » vide : « Encore rien ici ».
  - 7.22 : compteur « x tâches accomplies ! » ; nouvelle liste : une carte
    comme le formulaire d'une tâche (nom de la liste, première tâche,
    détail, échéance, heure, œuf / urgent) qui crée la liste ET sa
    première tâche d'un coup ; « Heure » sans « (optionnel) ».
  - 7.23 : pas de « ! » au compteur tant qu'il est à 0.
  - 7.24 : carte nouvelle liste : le champ à remplir est en gras (le nom,
    puis la première tâche). Partout : l'heure reste grisée tant qu'il n'y
    a pas d'échéance (effacer la date efface l'heure). Champs des
    formulaires : liseré rose au survol, jaune une fois sélectionné.
  - 7.25 : cliquer l'œuf ou le triangle ne vole plus le curseur du champ, et
    Entrée sur l'un d'eux valide le formulaire (avant : Entrée re-cliquait
    le bouton et annulait la couvaison au lieu d'enregistrer).
  - 7.26 : champs des formulaires dans l'appli : bleu au survol, bleu qui
    reste une fois cliqué. Carte de la première liste (accueil) : jaune
    au survol et une fois sélectionné (le rose reste aux pointillés).
  - 7.27 : mode sombre : case urgente rose-rouge profond (plus de brun),
    case douceur bleu nuit avec l'or du trèfle (plus de kaki).
  - 7.28 : mode sombre : rouge plus franc (moins violacé), case douceur
    graphite neutre (plus le duo bleu/jaune), « En cours » vert plus frais.
  - 7.29 : mode sombre : case urgente en carte sombre neutre, légèrement
    rosée, avec un fin liseré rouge (plus de fond brun).
  - 7.30 : mode sombre, case urgente calquée sur la carte de fichier de
    l'app Claude : fond prune très sombre, liseré vieux rose, accents rose-rouge.
  - 7.31 : liseré de la case urgente (mode sombre) retiré.
  - 7.32 : mode clair : fond de la case douceur en lin neutre au lieu du
    jaune (le titre et le halo restent dorés).
  - 7.33 : case douceur entre les deux (ivoire à peine doré), typo plus
    petite ; fond de page : dégradé fixe sur la fenêtre, du bleuté en haut
    vers un gris plus sombre et plus froid en bas (--bg-bottom).
  - 7.34 : bas du dégradé clair un peu moins gris.
  - 7.35 : fond de page remis comme avant la 7.33 ; fond douceur un rien
    moins vert.
  - 7.36 : phrase de motivation en IBM Plex Mono comme le compteur, en gras.
  - 7.37 : titre de la case douceur remis à la taille des autres titres
    (seules les deux propositions restent plus petites) ; tapis déroulé
    moins contrasté, et en mode sombre fortement assombri (filtre sur
    l'image, rien de redessiné) pour ne plus éblouir.
  - 7.38 : tapis moins « poussiéreux » : plus de filtre gris par-dessus ; à
    la place, deux gammes propres et peu contrastées (claire, et sombre pour
    le mode sombre) et une texture de laine plus légère.
  - 7.39 : compteur à la même taille que la phrase de motivation ; phrase
    encore plus grasse.
  - 7.40 : case urgente : un seul survol par ligne (le survol du texte se
    superposait à celui de la ligne) ; mode sombre : « En cours » un peu plus
    discret, survol des lignes en vert clair comme l'urgent ; compteur
    « x tâches accomplies cette semaine ! ».
  - 7.41 : carte du compteur, version « éditorial » (choisie parmi deux propositions) : « 3 tâches accomplies cette semaine » en Public Sans (chiffre gras), barre fine, phrase dessous en Newsreader italique, centrée, comme une citation.
  - 7.42 : chiffre du compteur en IBM Plex Mono (le 0 pointé) ; mode sombre :
    « Rien d'urgent pour l'instant » dans le ton du titre d'« En cours »
    (gris clair, graisse normale) au lieu du blanc.
  - 7.43 : sauvegardes : un lundi, si rien n'a été sauvegardé depuis le lundi
    d'avant, petite ligne « Dernière sauvegarde il y a X jours » à côté du
    bouton, jusqu'à la prochaine sauvegarde (clés « lastbackup » et
    « backupwatch », hors fichiers de sauvegarde). Le navigateur est prié de
    ne jamais vider ce stockage de lui-même (navigator.storage.persist).
    Correctif : une sauvegarde restaurée perdait les œufs (tâches en
    couvaison redevenues normales) et le sens d'affichage des listes ; les
    deux font maintenant partie de la photo de sauvegarde.
  - 7.44 : phrases : retrait des références trop françaises (Bretagne,
    mistral, Vendée, horloge comtoise, Vermot, Solex, pétanque, jeudi sans
    école…) ; la mobylette du facteur reste.
  - 8.0 : grand rangement, sans rien changer à l'écran ni aux données
    (vérifié par comparaison de captures, état par état, et d'un long
    scénario d'utilisation, avant/après). CSS : les retouches 7.x empilées
    en fin de feuille sont fondues dans leurs règles ; code mort retiré
    (ancien ajout par IA, ancienne synchro, classes et fonctions jamais
    utilisées). JS : gestes en double regroupés (voir RANGEMENT). Correctif :
    les textes saisis sont échappés (un « <b> » dans un titre s'affiche tel
    quel au lieu de mettre en gras).
  - 8.1 : un envoi dans « En cours » compte comme une tâche accomplie
    (compteur de la semaine et graphique de la corbeille ; un aller-retour
    compte deux fois ; clé « waitlog », sauvegardée). ⌘Z / Ctrl+Z annule le
    dernier geste (40 crans, en mémoire seulement), sauf dans un champ de
    saisie où c'est l'annulation du texte.
  - 8.2 : fenêtre de relance : « Pas de relance » tout en haut ; plus de
    bouton OK, une date choisie est prise directement.
  - 8.3 : compteur en machine à écrire (Courier Prime, comme la corbeille) ;
    phrase de motivation en Public Sans droite, disposition inchangée.
  - 8.4 : phrase du compteur en bleu acier demi-gras (variable --phrase :
    #3F6A8C en clair, #9CC0DC en sombre).
  - 8.5 : ⌘Z fiable : la pile d'annulation n'est plus vidée quand un autre
    onglet de l'appli est ouvert, et survit au rechargement (sessionStorage,
    seulement les clés modifiées). Phrase du compteur alignée à gauche, un
    rien plus bas.
  - 8.6 : compteur : nombre rouge en grand (1,6×), ligne du compteur
    rapprochée de la barre, phrase plus détachée ; flèche d'ordre des
    listes (▲/▼) plus discrète (opacité 0,45, pleine au survol).
  - 8.7 : « tâches accomplies cette semaine » : presque noir avec une pointe
    de bleu (--count-ink : #22303F clair, #E2EAF2 sombre). Marquer une tâche
    urgente ne la fait plus remonter en haut de sa liste : elle reste à sa place.
  - 8.8 : pointe de bleu du compteur un rien plus marquée (#1E3552 / #D5E3F3).
  - 8.9 : compteur et phrase en gras ; phrase un chouïa remontée (0,9rem).
  - 8.10 : compteur « tableau de bord » : à gauche le chiffre de la semaine
    en grand avec son libellé en petites capitales machine à écrire (plus de
    « ! »), au milieu la phrase entre deux filets, à droite le total des
    tâches ; barre fine (3px) en dessous. Sur téléphone : chiffre et total
    côte à côte, puis la barre, puis la phrase.
  - 8.11 : total réduit à « x tâches », en petit, au-dessus du bout de la
    barre, sans filet. Deux polices seulement : Public Sans (texte) et
    Courier Prime (titres, badges, compteur, corbeille) ; IBM Plex Mono et
    Newsreader (plus utilisée) retirées.
  - 8.12 : « Total : x » au bout de la barre, sur sa ligne, plus foncé.
    Listes : poignée ⋮⋮ et icônes ↪ ⚠ × seulement au survol de la ligne
    (toujours visibles sur écran tactile). Trèfle : plus d'air (propositions
    plus hautes et plus espacées, léger relief, « ou » en petites capitales).
  - 8.13 : « Total x » (sans deux-points) au-dessus du bout de la barre, plus
    discret (gris) ; barre de nouveau sur toute la largeur. Case urgente : le
    rond « ! » centré sur la hauteur du titre.
  - 8.14 : couleurs calmées : liseré des listes à leur couleur mais adouci ;
    badges en deux familles (rouge pour retard / aujourd'hui / relance,
    contour gris pour le reste, RDV compris) ; noms de liste en gris dans la
    case urgente et « En cours ».
  - 8.15 : « Rien d'urgent pour l'instant » (et son rond) dans le rouge de
    l'urgent, éteint, au lieu du blanc devenu illisible ; idem en sombre.
  - 8.16 : (abandonnée) le rouge éteint de « Rien d'urgent pour l'instant »
    plus soutenu (78 % au lieu de 55 %) — non gardé, on reste à 55 %.
  - 8.17 : mise en ligne (GitHub Pages) avec une icône pour l'écran
    d'accueil (apple-touch-icon) : une tête de faisan vectorielle en gros plan, façon gravure (d'après un dessin à l'encre) ;
    source : icon-faisan.svg. Sauvegarder sur iPhone / iPad : la feuille
    de partage du système s'ouvre (Enregistrer dans Fichiers, iCloud,
    AirDrop, Mail…) au lieu d'un téléchargement peu visible ; ailleurs, rien
    ne change. Aucune clé de stockage ajoutée ni modifiée.
  - 8.18 : installable comme une appli sur ordinateur (Chrome / Edge :
    « Installer » ; Safari Mac : Fichier > Ajouter au Dock) avec l'icône
    faisan : fichier manifest.webmanifest + icônes 192 et 512. Rien d'autre.
  - 8.19 : l'appli s'appelle « Sous le tapis » partout (onglet, en-tête,
    nom de l'icône installée, sauvegardes) ; plus aucune trace visible de
    « Fauconnerie ». Clés de stockage inchangées, anciennes sauvegardes
    toujours importables.
  - 8.20 : icône d'ordinateur (Chrome sur Mac) sans plaque blanche autour :
    icônes icon-faisan-mac-192/512.png déjà découpées à la forme macOS
    (coins arrondis, marge transparente), plus d'icône « maskable » dans le
    manifest — c'est elle que Chrome posait sur un fond blanc. L'icône
    iPhone (icon-faisan-180.png) ne change pas.
  - 8.21 : sur Android, l'appli charge manifest-android.webmanifest, avec
    l'icône pleine (icon-faisan-plein-192/512.png, « any » et « maskable »)
    qu'Android découpe à sa forme ; ordinateur : manifest.webmanifest
    (icône macOS). Rien d'autre.
  - 8.22 : œil du faisan plus vif : liseré blanc autour de la pupille et
    reflet blanc pur (icon-faisan.svg). Toutes les icônes régénérées sous de
    nouveaux noms « -v2- » pour éviter les anciennes en cache.
  - 8.23 : icône d'ordinateur avec un liseré blanc (4 %) qui suit la forme
    arrondie macOS, dessin réduit à l'intérieur (icon-faisan-mac-v3-*).
    Android et iPhone inchangés.
  - 8.24 : liseré blanc épaissi à 6 % (icon-faisan-mac-v4-*) : à
    l'installation, Chrome / macOS recadrent l'icône et mangeaient le
    liseré de 4 %.
  - 8.25 : case douceur fermée chaque matin, comme un gros bouton (titre +
    chevron). Au clic, le trèfle tourne comme une manivelle, la case se
    déploie et les deux propositions défilent, floues, comme une machine à
    sous, puis se posent sur les deux tâches du jour (la 2e un peu après).
    Le bouton ⟳ relance la même animation, en plus court. Ouverte une fois,
    elle le reste jusqu'au lendemain ; déjà faite : affichée ouverte.
    Nouvelle clé « fauconnerie-v2-luckyopen » (date d'ouverture seulement),
    hors annulation et sauvegardes. Animations coupées si le système
    demande moins de mouvement.
  - 8.26 : case ouverte : reclic sur le trèfle pour la refermer — la
    manivelle tourne à l'envers, les deux tâches s'effacent sans tourner et
    la case se replie. Au ⟳, le trèfle ne tourne plus (seuls les rouleaux). Tirage et choix du jour gardés. (Pas de fermeture une
    fois la tâche du jour faite.)
  - 8.27 : info-bulle du petit triangle d'ordre d'une liste : elle propose
    ce que fera le clic (« Récentes en bas ? » / « Récentes en haut ? ») au
    lieu de décrire l'état actuel, que la flèche montre déjà.
  - 8.28 : case urgente : le détail de la tâche (s'il y en a un) s'affiche
    sous son titre, en petit et discret, comme dans les listes.
  - 8.29 : case urgente : poignée ⋮⋮ à gauche de la case à cocher et
    visible seulement au survol, comme dans les listes ; textes à la même
    place qu'avant. Puce plus grosse, dans le rouge vif du titre, un peu
    plus à gauche ; détail un peu plus clair.
  - 8.30 : case urgente : poignée et case à cocher reviennent dans la ligne,
    à l'intérieur de la zone de survol (élargie vers la gauche, textes
    toujours à la même place) : on ne perd plus le survol en allant cocher.
    Case à cocher et poignée dans le flux, centrées sur la 1re ligne ;
    plus d'espace perdu entre la case et la puce. Puce un rien moins vive.
  - 8.31 : détail replié : une tâche qui a un détail montre un petit sigle
    (trois lignes) à côté de son titre ; clic sur le sigle, ou sur la ligne
    dans les listes, pour le déplier / replier (hauteur animée). Le choix est
    gardé par tâche et partagé avec la case urgente (là, seul le sigle
    déplie : la ligne garde son saut vers la liste). Nouvelle clé
    « fauconnerie-v2-notesopen » (seulement les tâches dépliées), préférence
    d'affichage hors annulation et sauvegardes. Flèches ↪ / ↩ dessinées en
    SVG (l'iPhone les remplaçait par son émoji, blanc sur carré gris).
    Petites vibrations (objet haptic) : tâche cochée, ligne ou liste
    soulevée, emplacement qui s'aimante, ligne posée, rouleaux du trèfle qui
    s'arrêtent — navigator.vibrate sur Android, interrupteur caché
    (<input switch>) sur iPhone iOS 18+.
  - 8.32 : flèche « en cours » vers le bas (la case est en dessous), retour
    vers le haut. Compteur : le gros chiffre prend la place du mot
    « tâches » (« 3 ACCOMPLIES / CETTE SEMAINE ») ; total sans le mot
    « Total », un rien plus petit et plus près de la barre. Vibrations
    revues : depuis iOS 26.5, Safari ne donne plus le tic pour un clic
    déclenché par le code (8.31 muette sur iPhone) ; seul un vrai toucher
    sur l'interrupteur (ou son label) le donne. haptic.attach() pose donc
    un label transparent, relié à l'interrupteur caché, sur les cases à
    cocher (listes, case urgente, trèfle), le sigle du détail et la case
    trèfle fermée ; il fait suivre le clic à l'élément d'origine. Glisser
    et rouleaux restent sans tic sur iPhone (pas de toucher à ce moment).
    Sur Android, les rouleaux du trèfle « cliquettent » à chaque tâche qui
    défile, comme une roue de sélection.
  - 8.33 : flèche « en cours » qui descend puis tourne à gauche (retour :
    elle monte puis tourne à gauche). Plus d'air entre le gros chiffre et
    « accomplies ». Vibrations : plus de tic à l'ouverture de la case trèfle ;
    tic au ⟳ et à la fermeture par le trèfle ; tâche cochée plus marquée sur
    Android (haptic.strong). Case urgente : un clic sur une tâche qui a un
    détail le déplie (sans détail : on va toujours à la liste).
    Formulaires (nouvelle tâche, modification, nouvelle liste) : œuf et
    triangle à gauche, Annuler puis le bouton qui valide tout à droite.
  - 8.34 : flèche « en cours » : descend puis tourne à droite (↳) ; le
    retour est la même tournée d'un demi-tour (↰). Vibrations : plus de tic
    en dépliant un détail ; tic de retour à l'ouverture de la case trèfle.
    Case urgente : plus de voile gris au toucher (tap-highlight), pas de
    survol qui reste collé sur écran tactile ; une tâche sans détail ne
    réagit plus au clic (plus de saut vers la liste). Compteur en bloc : le
    chiffre à gauche, « accomplies » calé sur le haut du chiffre et « cette
    semaine » sur sa ligne de base, de 0 à 99.
  - 8.35 : survol de la case urgente rétabli sur écran tactile (seul le voile
    gris du toucher reste supprimé). Compteur en bloc justifié : 1re ligne
    « chiffre + accomplies », 2e ligne « cette semaine », les deux de même
    largeur. Si la 2e est plus large, l'espace entre le chiffre et le mot
    s'agrandit (CSS) ; si la 1re l'est, « cette semaine » s'espace lettre
    par lettre jusqu'à la même largeur (fitCountBlock, après chaque mise à
    jour et au chargement des polices).
  - 8.36 : compteur : plus d'étirement ; « cette semaine » simplement calé
    à droite sous « accomplies » (fitCountBlock retiré). Titres des listes
    dans la couleur de leur liste. En renommant une liste (double-clic sur
    son titre), une rangée de pastilles de la gamme permet de changer sa
    couleur, appliquée tout de suite ; elle est écrite dans la liste
    elle-même (clé « customcats », déjà sauvegardée et annulable).
    mergeCustomCategories() recopie aussi la couleur des listes déjà
    chargées, pour que ⌘Z et les autres onglets la suivent. À la création,
    couleur toujours choisie automatiquement.
  - 8.37 : compteur en vrai bloc, de 0 à 99 : les deux lignes ont la largeur
    de « cette semaine » ; avec un chiffre, l'espace avant « accomplies »
    s'agrandit (CSS) ; avec deux, le chiffre rapetisse juste assez pour
    tenir (jusqu'à 62 % ; au-delà, « cette semaine » s'espace un peu) —
    fitCountBlock(). Lignes un rien plus serrées. Case urgente sur écran
    tactile : case à cocher et boutons toujours visibles (comme dans les
    listes) ; avant, l'iPhone gardait le 1er toucher pour faire apparaître
    ces éléments, et il fallait toucher deux fois pour déplier le détail.
    Case trèfle refermée par le trèfle : plus de surbrillance tant que le
    pointeur n'en est pas sorti (classe « rest »). Titre de la case :
    « Une petite en passant ? ».
  - 8.38 : case urgente sur écran tactile : case à cocher et boutons de
    nouveau cachés au repos ; le toucher d'une ligne les fait apparaître
    (classe « revealed ») ET déplie son détail, en un seul toucher. Le
    dévoilement au survol est réservé aux souris (@media (hover:hover)),
    sinon l'iPhone garde le 1er toucher pour lui. Cachés, case et boutons
    ne réagissent pas (pas de coche par mégarde). Compteur : « accomplies »
    et « cette semaine » plus serrés, bloc rapproché de la barre.
  - 8.39 : listes et « En cours » sur écran tactile : ↳ ⚠ × cachés au
    repos (ils étaient toujours visibles à 65 % depuis la 8.12), dévoilés
    par le toucher de la ligne (classe « revealed », une ligne à la fois),
    comme la case urgente ; cachés, ils ne réagissent pas. Le survol ne les
    dévoile plus qu'à la souris, et un clic de souris ne les laisse plus
    affichés (focus clavier seulement : :has(:focus-visible)). Le sigle du
    détail suit directement le titre (avant le nom de liste et le badge),
    collé au dernier mot (titleWithToggle), partout. Mode clair : fond uni, teinte claire du
    bleu ardoise de l'icône (#34495A), plus de dégradé.
  - 8.40 : fond clair : sauge pâle, lumineuse et peu grise (#ECF4EB), uni,
    choisi parmi quatre pistes (ciel, lin, sauge, ardoise).
  - 8.41 : sauge beaucoup plus claire (#F5F9F4). Boutons du bas Corbeille et
    Restaurer : fond blanc et fin liseré, texte dans une ardoise de la
    famille de l'icône (--btn-ink) au lieu du mauve ; Sauvegarder garde sa
    teinte bleu-vert.
  - 8.42 : fond un rien plus clair et plus froid (#F7FAF9). Liseré gardé
    pour Corbeille seulement ; Restaurer, fond blanc sans liseré.
  - 9.0 : version majeure à la demande d'André-Pierre (détail replié, flèches
    dessinées, vibrations, compteur en bloc, couleurs des listes, fond
    sauge des 8.31–8.42). Restaurer aussi large que Sauvegarder (deux
    caractères de plus de marge, police à chasse fixe). « + Nouvelle
    catégorie » devient « + Nouvelle liste », sur fond blanc, pointillés
    gardés.
  - 9.1 : bloc « accomplies / cette semaine » un chouïa plus haut par rapport
    à la barre. Titres des tâches toujours avec une majuscule initiale
    (capFirst, appliqué dans getEffective et à l'affichage de la corbeille) :
    rien n'est réécrit dans le stockage, une tâche modifiée est simplement
    enregistrée avec sa majuscule.
  - 9.2 : préparation de la synchro en ligne, sans aucun changement visible
    ni de données. Tous les accès au stockage passent par une porte unique
    (Store), et la réception des changements d'un autre onglet devient la
    fonction applyExternalChange(), réutilisable pour un autre appareil.
    Clés, valeurs et sauvegardes strictement identiques.
  - 9.3 : en renommant une liste (titre + couleurs), ses propres tâches et ses
    boutons (+, sens, poignée, ×) s'estompent comme le reste ; seuls le champ
    du titre et les pastilles de couleur restent actifs.
  - 9.4 : Échap referme le renommage d'une liste même quand le curseur n'est
    pas dans le champ du titre (il ne l'était pas après le double-clic).
  - 10.0 : nouveau rangement des données en fiches (voir FICHES), sans aucun
    changement visible : une fiche par liste avec des tâches à identifiant
    stable, une fiche « moi » (corbeille, journal en cours, ordres). Migration
    automatique et vérifiée ; les anciennes clés restent intactes, en
    secours. La corbeille note désormais la tâche d'origine. Sauvegarder
    exporte le nouveau format ; les anciennes sauvegardes restent lisibles.
    Prochaines étapes déjà décidées : Firebase (plan Spark, Firestore
    europe-west1, mode production, connexion Google) ; plume
    plume-connexion.svg à droite du titre (~44 px, pointe au-dessus ; bleu
    --accent connecté, #B08478 déconnecté) ; bouton « Partage » en bas
    (panneau comme la corbeille, Échap le ferme) avec carnet d'invités par
    lien (copier / WhatsApp), noms à cocher dans l'édition d'une liste ;
    plus tard, phrases d'encouragement par utilisateur (celles du faisan
    restent la base, dans le code).
  - 10.1 : connexion et synchro en ligne (voir SYNCHRO EN LIGNE) : plume à
    droite du titre, connexion Google ou e-mail + mot de passe, listes
    recopiées en ligne et fusionnées entre appareils ; sans connexion, rien
    ne change. Sur une autre page (restauration, synchro), une liste
    disparue disparaît aussi de l'écran. Testée d'abord sur essai.html.
  - 10.2 : partage des listes (voir PARTAGE DES LISTES) : bouton « Partage »
    en bas avec le carnet et les liens d'invitation (copier / WhatsApp) ;
    « Partagée avec » dans le renommage d'une liste ; pastilles d'initiales ;
    un invité n'efface que ses propres tâches ; chacun son compteur et sa
    purge ; nouvelles règles firestore.rules (à recoller dans la console).
  - 10.3 : plume retouchée (réglée au banc d'essai le 22/10/2026) : dessin
    « fentes de faisan » (fentes qui plongent vers le rachis, comme une vraie
    plume), 28 px, tomate claire --plume-off (#E5675A / sombre #F2847A) avec
    un halo très léger ; pointe calée sur le bord droit des cartes, titre
    reculé d'autant (padding-right 45px) ; au survol, s'incline de 9° vers
    la droite (pivot au centre).
  - 10.4 : plume et titre décalés de 24 px vers la gauche : la pointe de la
    plume s'aligne sur le bout droit de la barre de comptage ; même écart
    entre le titre et la plume.
  - 10.5 : fenêtre de connexion : titre et « Mot de passe oublié ? » centrés,
    « Se connecter » et « Créer un compte » de même largeur ; bouton Partage :
    survol (et panneau ouvert) en jaune --lucky-gold, texte foncé ; Restaurer
    reprend le survol bleu de Sauvegarder.
  - 10.6 : quand la connexion est possible (Sync.available, body.cloud),
    Sauvegarder / Restaurer quittent le bas de page pour deux petits liens
    « Copie de secours » / « Restaurer » dans la fenêtre de la plume ; le
    rappel de sauvegarde devient « Connecte-toi pour ne jamais perdre tes
    listes » (clic = la plume), et disparaît une fois connecté. Sans
    Firebase, rien ne change. Restaurer en étant connecté : les listes
    partagées et le carnet gardent leur état actuel (seules mes listes non
    partagées sont remises) ; une sauvegarde d'avant le format 10 ne se
    restaure pas connecté. Partage : survol jaune citron clair
    (--share-hover). « rejoint ton carnet de contacts ».
  - 10.7 : volet sur chaque liste : petite flèche en bas à droite
    (.cat-fold) qui replie la liste sur son bandeau (titre, ajout express,
    poignée), avec le nombre de tâches restantes ; on peut toujours la
    déplacer. Elle se rouvre quand on y ajoute une tâche (express ou « + »)
    ou quand on glisse une tâche dessus. Mémorisé par appareil
    (localStorage « sltapis-volets », hors sauvegarde et hors synchro).
  - 10.8 : synchro sur l'icône d'écran d'accueil (iPhone) : si le verrou
    « un seul onglet parle à Firebase » n'arrive pas en 4 s, page à l'écran,
    l'onglet le reprend (l'icône restait sinon débranchée, avec « tout est à
    jour » et ses anciennes listes). Et un changement arrivé d'ailleurs pendant qu'une fenêtre ou une
    édition était ouverte (ex. les listes en ligne arrivant pendant la
    fenêtre de connexion : liste partagée absente sur l'icône d'écran
    d'accueil) n'est plus perdu jusqu'au rechargement ; il s'affiche dès
    que la fenêtre se ferme (externalPending).
  - 10.9 : dans la fenêtre de la plume (connecté), une ligne de diagnostic
    (fin du compte, fin du compte connu de l'appareil, branché ou en
    attente, listes en ligne dont celles des autres, dernière erreur) et
    « Réparer cet appareil » (oublie l'état de synchro de l'appareil : au
    rechargement, ses listes sont remplacées par celles du compte).
  - 10.10 : « Continuer avec Google » propose toujours le choix du compte
    (prompt select_account) au lieu de reprendre d'office celui déjà ouvert
    dans le navigateur.
  - 10.11 : « Réparer cet appareil » retiré (inutile en usage normal) ; la
    ligne de diagnostic sous la plume reste.
  - 10.12 : le petit chiffre à droite du compteur montre les tâches qui
    restent à faire (avant : le total des tâches dans les listes).
  - 10.13 : « Continuer avec Google » marche du premier coup sur iPhone :
    Firebase est préchargé à l'ouverture de la fenêtre de la plume (bouton
    « Un instant… » le temps du chargement) et la fenêtre Google s'ouvre
    dans le geste (avant, chargée après coup, elle était bloquée sans
    message). Petit chiffre du compteur dans la teinte de la barre vide.
  - 10.14 : seul le texte du titre déroule le tapis (avant : toute la ligne,
    y compris l'espace autour de la plume — sur un petit téléphone, un doigt
    qui ratait la plume déroulait le tapis) ; zone de toucher de la plume
    agrandie (::before invisible). Rien ne bouge à l'écran.
  - 10.15 : listes de courses (voir LISTES DE COURSES) : interrupteur à la
    création, conversion dans le renommage, rond creux qui raye sans faire
    tourner le compteur, quantités, crayon pour modifier un article,
    saisie en bas avec suggestions, Trier, Vider les
    rayés, hauteur bornée avec défilement interne ; hors purge et
    corbeille ; règles firestore.rules (type) à recoller dans la console.
    Testée d'abord sur essai.html (banc local).
  - 10.16 : rond creux des listes de courses plus petit (14 px au lieu de
    18), même place, texte aligné comme avant.
  - 10.17 : liste de courses en feuille de cahier (papier crème, lignes
    bleu pâle, marge rouge juste à gauche des ronds, plus de liseré
    coloré à gauche) ; quantités à l'encre rose bien visible (le rouge
    reste aux urgences) ; rond
    11 px. Clair, sombre et téléphone vérifiés sur le banc.
  - 10.18 : marge à la couleur de la liste, pile entre la poignée et le
    rond ; 4 px d'air de plus à gauche des ronds ; papier perle très claire, liseré
    très fin à la couleur de la liste et ombre plus nette pour se détacher
    du fond ; repliée, un clic n'importe où sur la carte la déplie ;
    texte des articles posé sur sa ligne ; un peu d'air avant Trier / Vider ;
    barre de défilement toujours visible quand la liste dépasse (iPhone
    compris) ; papier perle avec une pointe de jaune ; bandeau « Une petite
    en passant ? » en citron givré (--lucky-bg, choisi au nuancier) ; tous
    ses accents (surbrillance, liserés des propositions, textes) en jaune
    citron --lucky-lemon au lieu de l'or --lucky-gold, qui ne sert plus
    qu'au bouton « Nouvelle liste » du premier lancement.
  - 10.19 : urgences en améthyste (--urgent, --urgent-soft, --urgent-ink :
    case urgente, tâches urgentes, échéances dépassées, survol des croix,
    messages d'erreur), cousine du mauve du logo, choisie au nuancier ; picto
    de la case urgente = le triangle des boutons urgents (triangleSvg) ;
    « 1 seul point urgent » / « x points urgents ».
    Listes de courses : détail (note) sur chaque article, comme dans
    les autres listes — champ « Détail » dans le crayon, sigle à côté de
    l'article qui déplie / replie le détail (toucher la ligne raye toujours) ;
    ouverte, un clic sur le bandeau à côté du titre replie la liste (le
    titre garde son double-clic pour renommer). Plume : halo adouci.
    Titre et plume connectée au vert du logo (--logo-green). Liste de
    courses repliée : la saisie reste, on ajoute sans la déplier.
    Chiffre du compteur en améthyste.
  - 10.20 : cartes à nouveau alignées : les deux colonnes de listes sont
    strictement égales (minmax(0, 1fr) + min-width:0 sur .category) — avant,
    un contenu large (liste de courses, adresse sans espace…) élargissait
    sa colonne et les bords droits ne tombaient plus juste. Phrase de
    l'essuie : « nonante degrés » (numérotation belge).
  - 10.21 : le lien « Convertir en liste de courses / normale » (renommage
    d'une liste) ne réagissait pas : pendant le renommage, la règle qui
    estompe le reste de la carte (body.has-editing … > *:not(...)) ne
    l'exceptait pas — grisé et pointer-events:none depuis la 10.15.
    Ajouté aux exceptions (:not(.cat-convert)).
  - 10.22 : coller plusieurs lignes dans une liste normale (champ express à
    côté du titre, ou champ « Nouvelle tâche » du +) crée une tâche par
    ligne, dans l'ordre collé ; puces (-, *, •, [ ], 1.) retirées, lignes
    vides ignorées, 100 lignes max. Une seule ligne : collage normal.
    Sert à importer une to-do préparée ailleurs (par ex. par Claude).
  - 10.23 : relance arrivée (tâche « en cours » dont la date est passée,
    revenue dans la case urgente) en améthyste comme les autres urgences :
    la 10.19 avait recoloré l'urgent mais oublié ces 4 règles, restées en
    framboise (--relance). Le badge « Relance JJ/MM » garde son libellé.
    --relance ne sert plus qu'au rappel de sauvegarde. Plume déconnectée
    en gris (--plume-off = --ink-faint) au lieu de tomate.
    Petite mention sous la plume (#plumeTag) : « Hors ligne » quand on n'est
    pas connecté ou que le réseau manque (navigator.onLine, événements
    online/offline), « Souci de synchro » en cas d'erreur ; rien pendant la
    connexion ni pendant un envoi (« pending » passe à chaque modif). Sans
    réseau, la plume repasse en gris même connectée.
    Listes de courses rebaptisées « Mémo / shopping » à l'écran
    (interrupteur de création, « Convertir en… », bulle) — le code garde
    type:"courses". Effet papier glacé sur ces cartes : bande de lumière en
    biais (--gloss), bas légèrement ombré (--gloss-shade), fin liseré de
    lumière en haut. En % de la carte : chaque mémo, de hauteur différente,
    a son reflet un peu ailleurs ; en plus, 5 réglages d'angle et de place
    (--gloss-a, --gloss-p) pris dans l'ordre d'affichage des mémos : deux
    mémos voisins n'ont jamais le même reflet.
  - 10.24 : glisser-déposer. Défilement automatique de la page : zone
    élargie (max(120 px, 18 % de la fenêtre), avant 50 px), il continue
    tant que le pointeur reste dans la zone (boucle requestAnimationFrame,
    avant : seulement quand la souris bougeait), vitesse progressive
    (2 → 34 px par image, au carré de la profondeur ; au-delà du bord :
    vitesse max). Après chaque pas, l'emplacement est recalculé.
    Cartes de listes : plus de va-et-vient de l'emplacement — juste après
    un échange avec une carte, on ne revient pas vers elle tant que le
    fantôme n'a pas bougé de 48 px depuis l'échange.
  - 10.25 : couleurs. Encre urgente (--urgent-ink) #4A2580 → #5C2C92 :
    tout ce qui l'utilise suit (badges « En retard », tâches urgentes,
    relance…). Case urgente : titres, puces et tâches dans cette même encre
    (avant : titres noirs, puces améthyste) ; fond pâli (--urgent-soft mêlé
    au blanc de la carte, et moitié --accent-soft pour moins de rouge) et titre « N points urgents » pâli (encre mêlée
    au fond) — aucune nouvelle couleur, tout est dérivé des variables.
    Mémo / shopping : papier nacré léger (blanc → bleu glacé → lilas, tokens
    --memo-a/b/c) au lieu du bas grisé (--gloss-shade supprimé), liseré
    neutre bleuté, ombre légèrement bleutée.
    Case urgente, deuxième couleur : le nom de la liste d'origine prend la
    couleur de sa liste (--cat-color posé sur la ligne) ; badge « En
    retard » en terre cuite partout (--late / --late-soft, la seule couleur
    ajoutée). Trèfle du bandeau « Une petite en passant ? » dans le bleu de
    la phrase (--phrase). « Hors ligne » calé sur le bord droit du chiffre
    des tâches restantes, puis un rien plus haut et plus à droite, en
    accord avec l'arrondi du coin (right:12px, top:33px). Titre « Une
    petite en passant ? » en --phrase aussi (l'olive disparaît) ; fond
    citron un cran plus pâle (--lucky-bg #FBFADF → #FCFBE9) ; encre urgente
    finalement #562F96, un rien moins rouge.
    Trèfle du jour fait : le trèfle redevient un bouton, la case se replie
    (grisée, « Trèfle du jour fait ! », clé luckydoneclosed du jour) ; un
    clic dessus fait tourner le trèfle et lance une nouvelle tournée (deux
    nouvelles propositions, les tâches cochées exclues).
  - 10.26 : connexion sur iPad. Les champs e-mail / mot de passe (et la date
    de relance) passent à 16 px sur écran tactile : en dessous, Safari iOS
    zoome tout seul au toucher, et le doigt qui remettait la page en place
    tombait hors de la fenêtre et la refermait. La fenêtre de la plume ne se
    referme plus d'un toucher à côté quand un champ est rempli (le clavier se
    range, c'est tout ; la plume ou Échap la ferment), ni pendant un zoom.
    E-mail : à « Créer un compte », l'adresse est réaffichée en grand pour
    confirmation ; une faute de frappe probable dans le domaine (gmial.com,
    hotmail.con…) est signalée avec la correction proposée, dès qu'on quitte
    le champ.
  - 10.27 : « Copier les tâches » dans le renommage d'une liste (double-clic
    sur le titre), sous « Convertir » : copie les tâches pas encore cochées,
    une par ligne (« - titre », détail entre parenthèses, « [urgent] »,
    « [en cours] », quantité pour les courses), pour les coller ailleurs
    (par ex. chez Claude). Le lien affiche « Copié (N) » un instant.
  - 10.28 : le lien s'appelle « Copier (toutes les tâches de la liste) ».
  - 10.29 : case urgente, cohérence visuelle : le triangle allumé apparaît
    aussi sur les tâches arrivées là à cause de leur date (relance tombée,
    échéance dépassée). Pour elles il est inerte (.urgent-btn.auto, pas de
    clic) : la tâche reste urgente tant que la date est passée. Seules les
    tâches marquées urgentes à la main gardent le triangle cliquable.
  - 10.30 : bouton d'accueil « Go dépoussiérage » aux couleurs de la case
    « Une petite en passant ? » : fond citron givré (--lucky-bg), titre en
    bleu de la phrase (--phrase), pointillés et + en citron (--lucky-lemon),
    même survol (halo citron, carte qui se soulève d'1 px, + qui grossit
    un peu). Le + est dessiné en SVG, centré dans son rond à toute taille.
    Lien sous le bouton : « ou restaurer à partir d'une sauvegarde ». Champs de la
    carte « Nouvelle liste » du premier lancement : citron aussi. --lucky-gold
    ne sert plus nulle part (gardé dans :root, on ne supprime rien).
  - 10.31 : survol du triangle urgent d'une tâche (pas encore urgente) :
    jaune orangé (--lucky-gold, qui resservait plus), triangle qui se
    remplit un peu et grossit (zoom seul). Déjà urgente : même zoom, couleurs
    de l'urgence inchangées. Survol de la flèche « En cours » : couleurs de
    la case « En cours » (--wait-soft / --wait) ; survol de la croix : le
    bleu qu'avait la flèche (--accent-soft / --accent-strong). Même petit
    zoom au survol sur les trois boutons d'une ligne (× dans <span class="x">).
    Lien d'accueil sur deux lignes : « ou restaurer » (seul
    « restaurer » se souligne au survol), dessous, en petit, « (à partir
    d'une sauvegarde) ».
    NOUVEAUTÉS DANS LES LISTES PARTAGÉES (étage 1, sans serveur) : une tâche
    ajoutée par quelqu'un d'autre (base.by ≠ moi) est surlignée légèrement
    sur toute la largeur, avec « new Hiske » en haut à droite de la ligne
    (s'efface au survol pour laisser les boutons). Elle le reste au moins
    24 h après la première fois qu'elle a été affichée à l'écran (appli
    visible). Si elle arrive pendant que l'appli est à l'écran : un message
    en bas (« Hiske a ajouté « … » à Courses »). Pas de compteur sur la carte.
    Mémoire : clé locale sous-le-tapis-vu (hors fiches, propre à l'appareil)
    = { c: { idListe: seuil }, s: { cléTâche: date de première vue } } ; les
    tâches ne font que s'ajouter en fin de liste (un invité ne peut pas en
    faire baisser le nombre), donc seuls les index ≥ seuil peuvent être
    nouveaux ; le seuil avance quand les premières ne le sont plus.
    Première rencontre d'une liste : rien de nouveau (pas d'avalanche).
    En-tête des listes revu (choisi au banc d'essai) : le + suit le dernier
    mot du titre ; le champ express reste à côté du titre s'il tient en
    entier (8rem), sinon il passe à la ligne, avec l'invite « Nouvelle
    tâche… » ; les initiales des personnes vont en bas à droite de la carte.
  - 10.32 : textes de l'interface sans tutoiement (tournures impersonnelles
    ou « on ») : invitations, partage, connexion, messages d'erreur, rappel
    de connexion. Le tutoiement reste dans les phrases d'encouragement
    (compteur, toasts, défi de la semaine) et dans le message WhatsApp
    d'invitation (écrit d'une personne à une autre).
    Survols uniformisés : même petit zoom (×1,18, léger rebond)
    sur tous les boutons à icône — + d'une liste, croix d'une liste vide,
    tri ▲▼, poignée, repli, crayon des courses, détail d'une tâche,
    éclosion, ⟳ du trèfle (qui ne fait plus demi-tour), et les trois
    boutons d'une ligne. Variables --pop-scale / --pop-ease. Restent à part,
    exprès : la plume (s'incline) et le trèfle-manivelle (tourne).
    Triangle urgent : retour au mauve (le jaune orangé de la 10.31 est
    abandonné). Le survol montre l'effet du clic : pas urgente → il
    s'allume en mauve et grossit (« mettre urgent ») ; déjà urgente → il
    s'éteint en gris, vide, et rapetisse (« retirer d'urgent »).
    Case urgente : ses boutons ont les mêmes survols que dans les listes
    (flèche aux couleurs d'« En cours », triangle comme ci-dessus) ; au
    repos ils gardent le ton de la case ; le triangle inerte ne bouge pas.
  - 10.33 : police des tâches (choisie au banc d'essai) : Work Sans, rangées
    serrées. Réglable en un seul endroit dans :root : --font-task (police),
    --task-size (taille), --row-pad (haut/bas d'une ligne, avant 0.42rem).
    Concerne seulement le texte des tâches : listes, bandeau urgent, champs
    d'édition d'une tâche. Titres, noms de liste en Courier, compteur,
    phrase d'encouragement, badges et corbeille ne bougent pas. Pour changer
    de police : modifier --font-task et l'ajouter à l'@import Google Fonts.
    Case « En cours », thème clair : la tâche survolée se teinte à partir du
    fond de la case (vert d'attente à 8 %) au lieu du beige des listes.
    Cases à cocher : la coche (case bleue + ✓) apparaît au survol, avec le
    même petit zoom que les boutons à icône ; cochée, la case reste grise
    (avant : bleue) pour faire moins de bruit. Même coche au survol, dans
    l'encre mauve, sur les cases du bandeau urgent (recentrées sur la
    nouvelle taille de texte).
  - 10.34 : un chouïa moins serré : --row-pad 0.34rem, écart entre tâches
    0.1rem ; bandeau urgent revenu à l'interligne d'avant (0.3rem, 0.15rem).
    Listes mémo (courses) : police à part, IBM Plex Mono (choisie au banc
    d'essai), réglable dans :root : --font-memo et --memo-size. Concerne les
    articles, le champ « Ajouter un article » et le nom en édition.
  - 10.35 : plus d'air entre le titre d'une liste et ses tâches (0.35rem de
    plus) et sous le titre du bandeau urgent (0.55rem au lieu de 0.2rem) ;
    « En cours » inchangé. Pas des lignes calé sur celui des mémos (≈ 36 px
    pour une ligne) : --row-pad revient à 0.42rem, articles des mémos un peu
    resserrés (0.61rem au-dessus au lieu de 0.76rem). Glisser au doigt : une tâche ou une liste ne se
    saisit plus qu'après un appui tenu sans bouger (TOUCH_HOLD_MS = 280 ms,
    tolérance 10 px, voir afterTouchHold) ; sinon la poignée laisse défiler
    la page (touch-action:pan-y sur écran tactile). Évite les tâches
    attrapées par inadvertance en balayant l'écran. Souris : inchangé.
  - 10.36 : alignements. Une seule colonne pour les marqueurs et une pour le
    texte, partout : le rond des mémos (marge gauche 7.5px au lieu de
    11.5px) et la puce du bandeau urgent (left -0.17rem, padding du texte
    1.45rem au lieu de 1.65rem) tombent pile sur le centre des cases à
    cocher des listes, et leur texte commence au même endroit que celui des
    tâches. Bandeau urgent : la puce s'efface quand la case à cocher
    apparaît (survol ou toucher), pour ne pas se chevaucher.
    Mémos : titre et premier article descendus de quelques pixels, posés sur
    les mêmes lignes que le titre et la première tâche des cartes voisines.
  - 10.37 : petites icônes des lignes (↳ ⚠ × ; mémos : crayon ×) en
    surimpression : elles ne réservent plus de place à droite, le texte
    prend toute la largeur (moins de tâches sur deux lignes) ; au survol ou
    au toucher, elles se posent en bout de ligne sur un fondu (--ctl-bg).
    Essayées au banc et écartées : icônes en colonne (débordent sur la ligne
    du dessous), rond des mémos dans la marge (moins horizontal).
    Pleine page : bouton à deux flèches en diagonale en haut à droite de
    chaque carte (listes et mémos) ; la carte s'ouvre sur toute la hauteur,
    centrée (820px max), fond de page derrière ; même bouton ou Échap pour
    revenir. Ordre des icônes de ligne : ⚠ puis ↳ puis × (avant : ↳ ⚠ ×),
    pareil dans le bandeau urgent. État dans fullpageCat (pas dans les données), classe
    « fullpage » remise à chaque rendu. .wrap perd son isolation le temps
    de la pleine page (sinon la carte reste sous le fond).
  - 10.38 : mémos dans la police des tâches (--font-memo = --font-task ;
    IBM Plex Mono retirée de l'@import). Petit espace (0.6rem) avant le
    premier œuf et avant la première cochée (classe group-start). Une tâche
    ou un article qu'on coche reste CHECK_LINGER_MS (2,5 s) à sa place, puis
    descend avec les cochées, en fondu (lingering, en mémoire seulement ;
    on attend la fin d'une saisie ou d'un glisser) ; les articles rayés des
    mémos descendent donc aussi en bas. Mémos : saisie en haut, sous le
    titre, hors de la zone qui défile (buildCoursesParts → entry + foot),
    alignée sur la 1re tâche des cartes voisines ; hauteur de ligne des
    articles calculée sur --row-pad (même pas que les tâches) ; « + » de la
    saisie recentré sur le rond. Flèche d'ordre aussi sur les mémos
    (newestAtBottom : un mémo enregistre ses nouveaux articles en fin
    d'ordre, une liste en tête) ; bouton Trier retiré (sortCourses,
    coursesSorted supprimées). Icônes en surimpression rangées avec la
    règle .item-controls ; polices des champs d'édition sans !important.
    Case cochée bleu-vert tant qu'elle est encore à sa place (classe
    lingering), grise une fois descendue. Article ajouté à un mémo surligné
    3 s (just-added). Flèche d'ordre colorée seulement quand le sens n'est
    pas celui par défaut (classe custom).
  - 10.39 : au doigt, les icônes d'une ligne (tâches, bandeau urgent)
    s'effacent seules après 4 s (REVEAL_MS), au 2e toucher de la ligne ou
    au toucher d'ailleurs (revealRow / hideRevealed). Mémos : crayon et
    croix ne sont plus affichés en permanence au doigt. Défilement :
    plus d'overscroll-behavior:contain sur les mémos (au bout, la page
    reprend) ; à la molette, la page garde la main tant qu'on la fait
    défiler (wireCoursesWheel, PAGE_SCROLL_KEEP_MS). Mémos : on raye
    seulement par le rond (comme les cases) ; toucher / cliquer la ligne
    dévoile crayon et croix (au doigt) et déplie le détail, comme ailleurs.
    Bandeau urgent : boutons en surimpression (le texte prend toute la
    largeur), fond de survol --uhover opaque calculé sur --ub-bg. Zones de
    toucher agrandies (pseudo-élément ::after) : rond des mémos, pleine
    page, flèche d'ordre.
  - 10.40 : entrée dans l'appli simplifiée.
    Nouvelle liste : la fenêtre ne garde que le nom, l'interrupteur
    Mémo / shopping et Annuler / Créer (Entrée crée) ; la carte créée s'ouvre
    avec le curseur dans « Nouvelle tâche… » ou « Ajouter un article »
    (refocusQuickCat / refocusCoursesCat). Champs nl-task, nl-note, nl-due,
    nl-time, nl-items et leur logique retirés.
    Accueil sans liste : plus de compteur tant qu'il n'y a rien à compter
    (body.no-tasks : aucune tâche hors mémos, rien coché cette semaine) ; à
    sa place, un cadre aux couleurs du bandeau urgent (--ub-bg, --ub-title,
    désormais rangés avec les couleurs et partagés) avec « Ce qui dort sous
    le tapis n'est pas perdu... » (une ligne si possible, sinon coupée entre
    ses deux moitiés) ; tapis collé sous ce cadre (cardsRef) et bouton
    remonté (aim 0.42 ordi, 0.32 téléphone). Lien sous le bouton : sans
    compte « ou se connecter / pour retrouver ses listes » (ouvre la plume,
    où Restaurer est aussi) ; connecté ou sans plume (mode de secours) :
    « ou restaurer », comme avant — la restauration reste toujours à portée
    (cloudState, refreshWelcome). Sous la plume, sur l'accueil et sans
    compte : « Se connecter » en gris (#plumeLogin, body.signed-out) au lieu
    de « Hors ligne ». Dans la plume, « Copie de secours » seulement s'il y a
    une liste. Titre décalé (body.no-tasks / no-list header) pour que la
    mention sous la plume ne touche jamais le cadre suivant.
    Rappel du bas « Se connecter pour ne jamais perdre ses listes » : la
    fenêtre s'ouvre sous le lien (openLoginAt) et non plus près de la plume,
    hors de vue en haut de page.
    Tapis qui se déroule : image SVG faite à la taille réelle en pixels
    (jusqu'à ×3) — Safari l'agrandissait depuis 400 px, d'où le flou sur
    téléphone (idem filigrane de l'accueil) ; en sombre, ni lustre ni
    marbrures (taches) ; « Hors ligne » / « Se connecter » masqués tant que
    le tapis est sorti (body.tapis-out).
    Petits messages (#toast) : durée selon la longueur (3,5 à 7 s, avant
    1,9 s), pause au survol, clic pour fermer, deux lignes sur téléphone ;
    aux couleurs de « Une petite en passant ? » (--lucky-bg, --phrase), fins
    et carrés ; étape = même case en gras. « Catégorie créée » devient
    « Liste créée ». Flèche de « Une petite en passant ? » retirée.
    Flèches pleine page discrètes comme leurs voisines (opacité 0.5, pleines
    au survol de la carte ; en pleine page, bien visibles).
    Sombre : « En cours » plus frais et effacé (--wait-soft #16292B, avant
    #142C29) ; fond urgent un rien plus présent (--ub-bg propre au sombre).
  - 10.41 : poignée des listes (.cat-grip) dans la marge, à gauche du titre,
    autant d'air côté liseré que côté titre (titre décalé de 0.3rem :
    padding-left de .cat-head) ; à la souris, visible au survol de la carte
    seulement ; en haut à droite ne restent que la flèche d'ordre et la
    pleine page. Prénom composé → deux initiales (André-Pierre → AP,
    initialOf) ; pastilles allongées au besoin, moins serrées. Rien
    d'enregistré : les listes déjà partagées suivent d'elles-mêmes.
    Texte tapé dans l'ajout express puis clic sur « + » : le formulaire
    détaillé s'ouvre avec ce texte (addPrefill) ; Annuler l'efface.
    Tapis qui se déroule : ×2 au plus (×3 en 10.40, 1er déroulé lourd sur
    iPhone) et préparé de nouveau en douce quand la page change de hauteur
    (ResizeObserver), pour que le clic parte tout de suite.
  - 10.42 : poignée des listes en bas à gauche de la carte, couchée
    (rotate 90°), pendant de la flèche du volet en bas à droite, visible en
    permanence comme elle ; la place à gauche du titre (10.41) marchait mal.
    Titres revenus comme en 10.40 (plus de décalage de .cat-head).
  - 10.43 : poignées des tâches (.item .drag-handle) calées sur la 1re ligne
    (line-height 18px + 0.15rem en haut : même centre que la case, l'œuf et
    le rond des mémos), au lieu du milieu d'une tâche sur plusieurs lignes.
    Picto du détail plus grand (16 px) et dans le jaune du trèfle foncé ;
    survol / ouvert sur --lucky-bg ; reste mauve dans la case urgente.
    Liste repliée : tâches restantes dans une bulle à la couleur de la liste
    (chiffre recentré : ceux de Courier Prime sont hauts) ; carte repliée un
    peu plus haute (2.1rem en bas) pour saisir la poignée sans attraper le
    titre. Texte des mémos un peu adouci (encre à 78 %). « En cours » :
    marge droite vérifiée, déjà comme ailleurs.
  - 10.44 : poignées de la case urgente calées sur la 1re ligne aussi
    (oubliées en 10.43). Bulle du nombre de tâches en Public Sans (les
    chiffres de Courier Prime ne se centraient pas pareil selon le
    navigateur). Phrase du jeudi : « L'autre prépare un coup fourré. »
  - 10.45 : listes partagées — étiquette « new – AP » (initiales, avant le
    prénom) et nouvelle « modif – H » : qui a changé le texte, le détail ou
    l'échéance d'une tâche, ou un article de mémo (overrides editBy / editAt,
    posés par markEdited, fusionnés et synchronisés avec les modifications ;
    pas la coche ni l'urgence). Visible 24 h après la première vue (mémoire
    locale sous-le-tapis-vu, champ m). Les étiquettes s'affichent aussi chez
    l'auteur (newItems / editedItems) ; le message en bas seulement pour ce
    que font les autres (« Hiske a modifié … dans … »). Le texte d'une ligne
    marquée garde 5.4rem à droite pour l'étiquette. Règles Firestore
    inchangées.
    Picto du détail toujours dans sa pastille ronde jaune (même fond, ouvert
    ou non ; plus foncée au survol). Liste repliée : flèche d'ordre masquée
    (se confondait avec celle qui rouvre). « Une petite en passant ? » calée
    à droite, trèfle à l'aplomb de la plume, titre qui finit où finit
    « Sous le tapis » ; ⟳ passe à gauche. Bouton « + Nouvelle liste » en
    citron givré, pointillés citron, petit zoom et halo au survol.
  - 10.46 : fenêtre « Rappel de relance ? » revue (askRelance, classe
    relance-ask) : titre en tête, petit et en mauve ; « Aucune relance »
    (« Plus de relance » pour un report) sur toute la largeur, curseur dessus
    à l'ouverture ; dessous, une rangée de petits boutons de même largeur
    (1 sem. / 2 sem. / 1 mois / date d'échéance s'il y en a une / calendrier
    en pictogramme, avec le vrai champ date invisible posé dessus : pas de
    zoom sur iPhone). Tous pareils : fond teinté (--wait 12 %), sans bordure,
    graisse normale, texte --phrase ; survol citron givré à fin liseré citron.
    La date exacte d'un délai est dans son infobulle. Les autres petites
    fenêtres (échéance au retour, plume) gardent leur forme.
  - 10.47 : petites fenêtres sans liseré extérieur (.relance-pop : border 0).
    Relance et retour d'« En cours » : titre mauve dans un petit onglet
    citron givré ; boutons teintés « En cours » au repos, citron givré au
    survol, sans liseré. Retour d'« En cours » (askBringBack) dans la même
    forme : trois petits boutons « Garder », « Effacer », calendrier (date
    prise directement, plus de champ ni de OK ; CAL_SVG partagé). Plume :
    boutons sobres (fond teinté d'accent, sans bordure, coins doux, texte
    --phrase, survol un cran plus soutenu), champs un peu plus fins. Règles
    .rp-date / .rp-ok retirées (plus utilisées).
  - 10.48 : fenêtre « Nouvelle liste » : interrupteur « Liste mémo –
    shopping » ; un clic ou un toucher en dehors de la fenêtre annule
    (écouteur pointerdown posé à l'ouverture, retiré à la fermeture). Titre
    de « En cours » en mauve : nouvelle couleur --title-mauve (rangée avec
    --ub-title), partagée avec le titre des petites fenêtres de tâche.
  - 10.49 : titre des petites fenêtres de tâche (relance, retour d'« En
    cours ») sans l'onglet citron de la 10.47 : mauve seul. Phrase « Une case
    non cochée est une promesse ; une case cochée, un acte authentique. »
    sans guillemets ni « jurisprudence de cour de récré ».
  - 10.50 : titre de « En cours » en deux morceaux insécables (« En cours - »
    / « La balle est dans leur camp ») : trop étroit, il se coupe après le
    tiret. Une tâche dans « En cours » ne porte plus la marque « new » /
    « modif » (elle gardait le surlignage sans l'étiquette). Essayés au banc
    et écartés : liseré de la couleur du survol sur les boutons des petites
    fenêtres, onglet citron autour des titres (« fait magasin de glace »).
  - 10.51 : titre de « En cours » revenu en --ink-soft (mauve en 10.48-10.50) ;
    --title-mauve retiré (plus utilisé). Petites fenêtres de tâche (relance,
    retour d'« En cours ») : fond blanc, titre --ink-soft, boutons dans le
    code du « + » des listes (.add-btn) sans sa bordure — papier --surface-2
    et --ink-soft au repos, --accent-soft et --accent-strong au survol. Choisi
    au banc parmi des codes existants (papier → citron, boutons du bas,
    10.47), pour ne plus inventer de teinte.
  - 10.52 : petites fenêtres de tâche dans le code de la fenêtre de la plume :
    fond blanc, boutons comme « Continuer avec Google » (--accent 12 %, texte
    --phrase), titre centré en --ink-soft (le gris de « Mot de passe
    oublié ? » ; bleu et mauve essayés au banc). Survol comme la case à
    cocher d'une tâche : plein --accent, écriture blanche comme sa coche.
  - 10.53 : une tâche « en cours » effacée (croix) ne compte plus comme
    accomplie si son envoi date de cette semaine (unlogWaitingThisWeek).
    Synchro : le carnet de contacts se fusionne personne par personne (avant,
    en bloc : un appareil pouvait écraser le contact ajouté par l'autre).
    Invitations : code court de 8 caractères (XXXX-XXXX, sans I L O 0 1),
    affiché avec le lien et joint au message ; case « Code d'invitation »
    dans la fenêtre de connexion (bouton Coller) et « On m'a donné un code »
    dans le partage ; le code, le code avec tiret ou le lien entier marchent
    (parseInviteInput). Anciens liens de 20 caractères toujours valables.
    iPhone / iPad dans Safari : nouveau venu → écran d'installation seul
    (avec le code à recopier) ; déjà des listes → bande « Installer »
    discrète, rien de bloqué. Icône, première ouverture : la connexion
    s'ouvre seule. Ordinateur / Android inchangés. Voir « 10.53 : sur
    iPhone / iPad » en bas du code.
    Modifications uniformisées : Annuler / Enregistrer aussi dans la
    modification d'une liste (Annuler et Échap remettent couleur et partage
    d'avant, catEditSnap ; clic à côté = Annuler partout) et d'un article de
    mémo ; double-clic sur un article de mémo pour le modifier ; + à côté du
    titre d'un mémo : article, quantité et détail. Copier une liste suit
    l'ordre affiché (flèche comprise). « Convertir en liste de shopping ou
    mémo ». Plus d'air avant « Nouvelle liste » ; une phrase sur le partage
    dans le panneau Partage.
    Case urgente : double-clic sur une tâche = sa fenêtre de modification,
    ouverte à sa place dans sa liste (rouverte si repliée) ou dans « En
    cours » (editUrgentEntry).
  - 10.54 : tâches cochées : elles descendent ensemble, 2,5 s après la
    dernière coche ; souris posée sur la liste, rien ne bouge tant qu'elle
    y reste ; la descente glisse doucement (FLIP, glideRows : 0,8 s, la
    cochée s'estompe un peu en route). Clic à côté d'une
    fenêtre de modification (liste, article de mémo) = Annuler, comme pour
    une tâche.
  - 10.55 : carnet : nom et initiales de chaque contact modifiables (crayon
    ou double-clic dans le panneau Partage ; champ « ini » du contact,
    personInitials) ; le nom du carnet passe avant celui que la personne
    s'est choisi. Mode sombre : papier des mémos uni #23231F, sans reflet
    ni liseré, comme en clair. Papier des mémos : blanc chaud #FCFBF7, uni (choisi au banc). Bord des
    listes : barre franche détachée, du titre à deux lignes du bas.
  - 10.56 : texte des articles de mémo à l'encre pleine (var(--ink), comme
    les tâches) au lieu de 78 % : plus lisible sur le papier blanc chaud.
  - 10.57 : écran de chat (voir ÉCRAN DE CHAT) : petit chat
    partagé, posé parmi les listes ; isSideList pour les exclusions.
  - 10.58 : fenêtre « Nouvelle liste » : Annuler / Créer sur la ligne de
    l'interrupteur, « + Ajouter un écran de chat » en dessous. Écran de chat : la saisie est un vrai champ visible (sélection à
    la souris, flèches, effacer au milieu du texte) ; le gros curseur ne
    s'affiche qu'en bout de texte, sinon curseur normal (classe mid).
  - 10.73 : ligne du titre des listes et mémos montée (--hd-lift) : flèche pleine page dans l'angle,
    à la hauteur de celle du chat et du jeu ; liste vide : la croix à la place de la pleine page ;
    téléphone : le + ouvre le clavier (focus pendant le clic) ; voyant du chat éteint aussi écran
    fermé ; « modif » vue n'est plus oubliée après 24 h (elle revenait en boucle).
  - 10.63 : duel de faisans (voir DUEL DE FAISANS) : petit jeu à deux en
    tour par tour, créé par « + Ajouter un duel de faisans » ; entraînement
    seul. Papier des mémos en blanc (--memo-a/b/c #FFFFFF, avant blanc chaud).
  - 10.67 : duel et écran de chat SANS PAPIER BLANC, à la largeur d'une liste ; poste de
    commande du duel posé sur la tôle ; Lancer et − / + taillés dans le métal (fond de la
    tôle, cadre et ombre dure), Lancer jamais grisé : il s'enfonce et remonte à chaque clic
    (.appui ; .locked = sans effet). Choix du faisan à gauche sous Lancer. Duel fermé : écran
    creusé, mince bandeau gris (celui de l'écran ouvert), fenêtre (.duel-win) centrée sur les
    faisans (--d-anc) ; ouverture/fermeture : le jeu garde sa taille et glisse (_preGlide /
    _postGlide, appelés par softHeight et foldSmooth), masqué par la fenêtre arrondie.
    Estompage : net seulement pendant un vol, la fête (jusqu'à la chute des plumes), un coup
    à découvrir ou quand c'est à nous de jouer. Pleine page : l'écran se rétrécit pour que
    tout tienne en hauteur (fitDuelFull, téléphone à l'horizontale). Vélo entier à la place
    de la roue (nom interne « roue » gardé). Punaise des écrans pleine seulement à son
    survol. Écran de chat : ouvert, au moins la taille de l'écran du duel (16/9), entrouvert
    à la hauteur de la rangée, sur ses derniers messages.
  - 10.66 : PUNAISE à la place de la flèche du volet (en bas à droite, et au pied des
    écrans de chat et de duel). Plantée droite (grise et discrète comme Agrandir et Trier, pleine au survol) = ouverte pour de bon ;
    retirée (clic) = la case se ferme. Fermée, la punaise attend couchée de travers, grise ;
    au survol la case s'entrouvre, un clic sur la punaise la garde ouverte, sinon elle se
    referme en partant. Au doigt : toucher la case l'entrouvre, toucher la punaise la garde.
    Plus aucun autre clic n'ouvre ni ne ferme (bandeau des mémos compris). foldSmooth : le
    haut de la case reste fixe, seul le bas glisse, la page ne saute plus (fold-still,
    keepRoomBelow). Survol : départ en douceur (SOFT_EASE .33,0,.2,1, 440–650 ms, 110 ms d'attente), fondu de l'aperçu et ombre en transition (plus de déclic). Survol aussi au mouvement de la souris (après un rendu, plus besoin de ressortir) ; l'attente après la punaise ne vaut que pour sa case. Barre du mémo cachée quand il est fermé, recalée au survol. Plus de transition sur la marge des tâches (cran en fin d'ouverture). Avant la punaise (même version) : la pile est abandonnée, et les cases ne se déplacent
    jamais seules (essayé puis écarté : fermées rangées en bas, remontée à
    l'ouverture). Survol souris = la case fermée s'entrouvre (.peek, sans
    toucher aux données), clic = ouverte pour de bon, à sa place. Au doigt :
    1er toucher entrouvre, 2e ouvre, toucher ailleurs referme. Liste fermée :
    aperçu pâle des premières tâches.
    Chat replié : la feuille de style cache les lignes (plus retirées).
    Duel fermé : la phrase dans le bandeau de l'écran du jeu (celui de « X a
    joué ! »), à bords perdus, texte à droite, au nombre d'or. Ouvertures
    douces : softHeight (la hauteur glisse, 380–620 ms, SOFT_EASE). Fermetures plus lentes (× 1,3, 560–780 ms au bouton) avec SOFT_CLOSE, qui démarre en douceur. Mémos en sombre : papier des listes (#1C2125).
  - 10.65 : volet des écrans de chat et de duel (repli sur une ligne,
    voyant vert du duel) ; toutes les cases repliées à la même hauteur
    (--fold-h, 127px : le mémo replié, resserré de 3 px, sert d'étalon) ;
    pleine page des écrans (même bouton que les listes, en haut à droite,
    voyant décalé à sa gauche ; papier du duel avec la même bande en haut).
    Écran du duel à la largeur de celui du chat (carte − 1,5rem, ordinateur
    et téléphone). Fermé, le chat garde son écran ; le duel fermé montre le
    jeu en filigrane (le canvas lui-même, object-fit, redessiné 1×/s) et la
    phrase d'état en clair, dans un rectangle façon bouton « Lancer ».
  - 10.64 : liste repliée : la bulle compte aussi les œufs en couvaison
    (eggsInCat), en plus des tâches à faire ; toujours pas les cochées.
  - 10.62 : écran de chat au doigt : toucher l'écran met le curseur dans la
    saisie sans preventScroll, le téléphone la remonte lui-même au-dessus du
    clavier (avant : seulement à la première lettre).
  - 10.61 : écran de chat sur téléphone (une colonne) : il grandit avec les
    messages jusqu'à 10 lignes (avant : 3, faute de liste voisine).
  - 10.60 : écran de chat : message non lu (d'un autre, pas encore vu sur cet
    appareil, CHAT_SEEN_KEY) → l'écran sort de sa discrétion,
    voyant vert sur la tôle en haut à droite (.chat-led), ligne « --- nouveau
    --- » (reste jusqu'à ce qu'on écrive : chatNewAt) ; lu dès qu'on passe
    dessus, le touche ou y écrit.
  - 10.59 : la saisie (textarea) s'agrandit avec le texte, 8 lignes au plus ;
    sur plusieurs lignes, curseur normal (classe multi). écran de chat à la largeur d'une liste moins 1,5rem, même marge
    en haut ; il prend la hauteur de sa rangée (3 lignes au moins) : plus de
    messages visibles quand une liste voisine est haute.
  - 10.74 : grand ménage, sans changement à l'écran : anciennes versions dans archives/,
    historique sorti vers ce fichier, 15 règles CSS en double fusionnées ; synchro : une salve
    de listes arrivées d'un coup (ouverture) ne donne plus qu'un seul rendu au lieu d'un par liste.
  - 10.75 : mémos — double-clic pour modifier sans rien rayer (le clic attend la fin d'un double-clic,
    souris), texte sélectionnable à la souris, coin corné en haut à gauche, papier gris très clair fermé ;
    champs du + ramenés en vue ; Partage en picto seul ; « Nouvelle liste » en case fantôme (halo citron
    au survol) ; fond d'une liste à la couleur d'une personne du partage (« Fond », choix propre à chacun,
    fiche « moi » listTint) ; jeu fenêtre ouverte : écran unique (le plus petit), bandeaux sur une ligne,
    phrases raccourcies, Revoir à gauche ; voyant en pleine page décollé de l'écran ; glisser : mêmes
    pointillés pour chat et duel, plus de vibration (marge DRAG_SWAP_MARGIN) ; dring dring = sonnette du vélo.
  - 10.76 : « En cours » en typo un peu plus petite (--task-size 0.85rem), sur deux colonnes sur ordi.
  - 10.77 : duel — « Nouvelle partie » réservée à celui qui n'a pas joué le coup final, une fois ce coup vu
    (l'autre lit « À … de relancer. ») ; téléphone couché : « Nouvelle partie » sur deux lignes, plus tronqué ;
    niveau « try hard » (interrupteur en face des faisans, avant le 1er coup) : trous plus petits, vent plus
    costaud, cible plus étroite (trace des coups gardée).
  - 10.78 : duel — chez le gagnant, « Nouvelle partie » masqué tant que l'autre n'a pas vu le coup final
    (marqueur « vu » écrit par l'appareil de l'autre), puis chacun peut relancer ; changer d'objet ne remet
    plus l'angle et la force à zéro.
  - 10.79 : duel — l'interrupteur try hard reprend le niveau de la partie d'avant ; « TRY HARD » en capitales, éteint dans le bleu pâli.
  - 10.80 : + au fond d'une liste : tout le cadre de saisie remonte en vue, avec un peu d'air (plus rogné) ;
    case fermée : la punaise qu'on vise reste sur place pendant que la case s'entrouvre ;
    « new » / « modif » : plus sur ses propres ajouts, 12 h au lieu de 24 ; plus de messages flottants des autres.
```
