document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const currentIP = window.location.hostname;
    const newAction = 'http://' + currentIP + ':9005/submit';
    form.action = newAction;
});
