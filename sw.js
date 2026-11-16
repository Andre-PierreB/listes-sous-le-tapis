// Sous le tapis — copie de l'appli gardée sur l'appareil (depuis la 11.2).
//
// À quoi ça sert : l'appli s'ouvre tout de suite depuis la copie gardée sur l'appareil, sans attendre
// le réseau (ni la page, ni les polices, ni le code de Firebase). Pendant ce temps, ce fichier va
// chercher la page en ligne et met la copie à jour : une version qu'on vient de publier apparaît donc
// à l'ouverture SUIVANTE (quitter et rouvrir, ou recharger deux fois).
//
// Ce fichier ne touche à AUCUNE donnée : ni les listes (localStorage), ni la synchro (Firestore), ni la
// connexion. Il ne garde que des fichiers : la page, les icônes, les polices, le code de Firebase.
//
// COUPER À DISTANCE : mettre ARRET à true et publier. À l'ouverture suivante, chaque appareil efface
// sa copie et retire ce fichier ; l'appli refonctionne comme avant la 11.2, sans rien faire à la main.
// (Le navigateur revérifie ce fichier en ligne à chaque ouverture de l'appli.)
//
// Seule la page de l'appli (l'adresse du dossier, ou index.html) est servie depuis la copie. Les bancs
// d'essai (essai.html, essai-jeu.html…) et les archives viennent toujours directement du site : quand on
// y travaille, chaque changement doit se voir tout de suite.
// Qui s'en sert : la page l'inscrit elle-même (fin du script, « copie gardée sur l'appareil »).
// Changer ce fichier : n'importe quel changement, même un commentaire, suffit pour que les appareils
// prennent la nouvelle version. Si le contenu gardé change de forme, augmenter le numéro de COPIE.
const ARRET = false;
const COPIE = "sous-le-tapis-copie-1";
const PREFIXE = "sous-le-tapis-copie-";
const ICI = new URL("./", self.location).href;   // le dossier de l'appli

// la page de l'appli : l'adresse du dossier ou index.html, quoi qu'il y ait après le « ? » (?invitation=… :
// même page) ; une seule copie, rangée à l'adresse du dossier. Toute autre page : pas servie d'ici.
const isApp = url => { const u = new URL(url); u.search = ""; u.hash = ""; return u.href === ICI || u.href === ICI + "index.html"; };
const good = r => r && r.ok && !r.redirected;

self.addEventListener("install", e => {
  self.skipWaiting();
  if(ARRET) return;
  // la page est gardée dès la première visite (sinon elle ne le serait qu'à la deuxième)
  e.waitUntil((async () => {
    try{
      const r = await fetch(ICI, { cache: "no-cache" });
      if(good(r) && r.type === "basic") await (await caches.open(COPIE)).put(ICI, r);
    }catch(err){ /* pas de réseau : ce sera pour la prochaine fois */ }
  })());
});

self.addEventListener("activate", e => e.waitUntil((async () => {
  const keys = await caches.keys();
  await Promise.all(keys.filter(k => k.startsWith(PREFIXE) && (ARRET || k !== COPIE)).map(k => caches.delete(k)));
  if(ARRET){ await self.registration.unregister(); return; }
  await self.clients.claim();
})()));

// la copie tout de suite si elle existe ; dans tous les cas on va chercher en ligne et on met la copie à jour
async function copyThenRefresh(e, key, request, isPage){
  const cache = await caches.open(COPIE);
  const kept = await cache.match(key);
  const fresh = fetch(request).then(async r => {
    if(good(r) && (!isPage || r.type === "basic")) await cache.put(key, r.clone());
    return r;
  });
  if(kept){ e.waitUntil(fresh.catch(() => {})); return kept; }
  return fresh;
}
// fichiers qui ne changent jamais à la même adresse (polices, code de Firebase d'une version donnée)
async function copyFirst(request){
  const cache = await caches.open(COPIE);
  const kept = await cache.match(request.url);
  if(kept) return kept;
  const r = await fetch(request);
  if(good(r)) await cache.put(request.url, r.clone());
  return r;
}

self.addEventListener("fetch", e => {
  if(ARRET) return;
  const req = e.request;
  if(req.method !== "GET") return;
  const u = new URL(req.url);
  // la page elle-même
  if(req.mode === "navigate"){
    if(!isApp(req.url)) return;   // bancs d'essai, archives : toujours directement du site
    e.respondWith(copyThenRefresh(e, ICI, new Request(ICI, { cache: "no-cache" }), true));
    return;
  }
  // icônes et fiches d'installation, à côté de la page
  if(u.href.startsWith(ICI) && /\.(png|svg|webmanifest)$/.test(u.pathname)){
    e.respondWith(copyThenRefresh(e, u.href, req, false));
    return;
  }
  // polices Google : la feuille (peut changer), puis les fichiers de police (ne changent pas)
  if(u.hostname === "fonts.googleapis.com"){
    e.respondWith(copyThenRefresh(e, u.href, new Request(u.href, { mode: "cors", credentials: "omit" }), false));
    return;
  }
  if(u.hostname === "fonts.gstatic.com" || (u.hostname === "www.gstatic.com" && u.pathname.startsWith("/firebasejs/"))){
    e.respondWith(copyFirst(req));
    return;
  }
  // tout le reste (synchro, connexion…) : rien à voir avec ce fichier, le navigateur fait comme d'habitude
});
