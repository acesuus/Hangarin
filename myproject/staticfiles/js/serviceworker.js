self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('hangarin-cache-v1').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/styles.css',
                '/static/css/responsive.css',
                '/static/js/scripts.js',
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js',
                'https://use.fontawesome.com/releases/v6.3.0/js/all.js'
            ]);
        })
    );
});
self.addEventListener('fetch', function(e) {
e.respondWith(
caches.match(e.request).then(function(response) {
return response || fetch(e.request);
})
);
});