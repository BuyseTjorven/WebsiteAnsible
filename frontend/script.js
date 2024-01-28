document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const currentIP = window.location.hostname;
    const newAction = 'http://' + currentIP + ':9005/submit';
    const progressBar = document.getElementById('progressBar');
    const progressBarContainer = document.getElementById('progressBarContainer');
    const messageBox = document.getElementById('messageBox');

    const wireguardButton = document.getElementById('wireguardButton');
    const nextcloudButton = document.getElementById('nextcloudButton');

    wireguardButton.addEventListener('click', function() {
        window.open('http://' + currentIP + ':30058', '_blank');
    });

    nextcloudButton.addEventListener('click', function() {
        window.open('http://' + currentIP + ':9001', '_blank');
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);

        progressBarContainer.style.display = 'block';
        updateProgressBar(0);

        let progress = 0;
        const interval = setInterval(function() {
            progress += 1;
            updateProgressBar(progress);
            if (progress >= 100) {
                clearInterval(interval);
                wireguardButton.disabled = false;
                nextcloudButton.disabled = false;
                wireguardButton.classList.remove('btn-secondary');
                wireguardButton.classList.add('btn-primary');
                nextcloudButton.classList.remove('btn-secondary');
                nextcloudButton.classList.add('btn-primary');
            }
        }, 1200); // 2 minutes duration

        fetch(newAction, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            showMessage(data.message);
        })
        .catch(error => {
            showMessage(error.message);
        });
    });

    function updateProgressBar(percent) {
        progressBar.style.width = percent + '%';
        progressBar.setAttribute('aria-valuenow', percent);
    }

    function showMessage(message) {
        messageBox.textContent = message;
        messageBox.style.display = 'block';
    }
});
