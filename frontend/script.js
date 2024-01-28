document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const currentIP = window.location.hostname;
    const newAction = 'http://' + currentIP + ':9005/submit';
    const progressBar = document.getElementById('progressBar');
    const progressBarContainer = document.getElementById('progressBarContainer');
    const messageBox = document.getElementById('messageBox');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);

        // Display the progress bar
        progressBarContainer.style.display = 'block';
        updateProgressBar(0);

        // Simulate a 3-minute progress update
        let progress = 0;
        const interval = setInterval(function() {
            progress += 1;
            updateProgressBar(progress);
            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 1800); // 1800ms * 100 = 3 minutes

        fetch(newAction, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Received content is not JSON');
            }
        })
        .then(data => {
            showMessage('Form submitted successfully: ' + JSON.stringify(data), 'success');
        })
        .catch(error => {
            showMessage('Error submitting form: ' + error.message, 'danger');
        });
    });

    function updateProgressBar(percent) {
        progressBar.style.width = percent + '%';
        progressBar.setAttribute('aria-valuenow', percent);
    }

    function showMessage(message, type) {
        messageBox.className = 'alert alert-' + type;
        messageBox.textContent = message;
        messageBox.style.display = 'block';
    }
});
