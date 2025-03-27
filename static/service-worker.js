const CACHE_NAME = "fuel-calculator-v1";
const urlsToCache = [
    "/",
    "/static/calculator.css",
    "/static/service-worker.js",
    "/static/manifest.json",
    "/static/icons/icon-192x192.png",
    "/static/icons/icon-512x512.png",
    "/static/icons/favicon.ico"
];

// Install event - cache assets
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log("Caching assets...");
            return cache.addAll(urlsToCache);
        })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        }).catch(() => {
            return caches.match("/");
        })
    );
});

// Activate event - remove old caches
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => cacheName !== CACHE_NAME)
                .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});
