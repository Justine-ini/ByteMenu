document.addEventListener('DOMContentLoaded', function() {
    const successAlert = document.querySelector('.alert-success');
    if (successAlert) {
        setTimeout(() => {
            successAlert.remove();
        }, 5000);
    }

    const errorAlert = document.querySelector('.alert-danger');
    if (errorAlert) {
        sessionStorage.removeItem('formData');
    }
});

// Optional: Preserve form data on errors
document.querySelector('form').addEventListener('submit', function() {
    sessionStorage.setItem('formData', JSON.stringify(Object.fromEntries(new FormData(this))));
});

