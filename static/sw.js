const CACHE = 'vokabella-v4';
const ASSETS = ['/', '/static/icon-192.png', '/static/icon-512.png', '/manifest.json', '/static/fonts/designer.woff2'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // API-Aufrufe (z.B. Sync mit PC) muessen immer live vom Server kommen,
  // niemals aus dem Cache - sonst sieht der Abgleich nie neue Serverdaten.
  if (e.request.url.includes('/api/')) return;
  // Cache-first fuer die App-Shell: App laeuft komplett offline (unterwegs, ohne PC/WLAN)
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(resp => {
        const copy = resp.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return resp;
      }).catch(() => caches.match('/'));
    })
  );
});
