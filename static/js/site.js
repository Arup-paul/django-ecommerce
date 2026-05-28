/* ShopDjango — global JS (placeholder, expand as needed) */
(function () {
    'use strict';

    // CSRF helper for fetch/HTMX requests (used later)
    window.getCsrfToken = function () {
        const el = document.querySelector('meta[name="csrf-token"]');
        return el ? el.getAttribute('content') : null;
    };

    // Auto-dismiss flash messages after 5 seconds
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
            setTimeout(function () {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }, 5000);
        });
    });
})();
