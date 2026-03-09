const appName = "tg-ctm"
const staticCacheName = `${appName}-{{ hash }}`

const files = [
  "/offline",
  {% for file in files %}"/{{ settings.STATIC_URL }}{{ file }}"{% if not forloop.last %},
  {% endif %}{% endfor %}
]

// Cache on install
self.addEventListener("install", event => {
  this.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName)
      .then(cache => {
        return cache.addAll(files);
      })
  )
});

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => (cacheName.startsWith(appName)))
          .filter(cacheName => (cacheName !== staticCacheName))
          .map(cacheName => caches.delete(cacheName))
      );
    })
  );
});

// Serve from Cache
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) return response;
        return fetch(event.request).catch(() => caches.match('/offline'))
      })
      .catch(() => {
        return caches.match('/offline');
      })
  )
});
