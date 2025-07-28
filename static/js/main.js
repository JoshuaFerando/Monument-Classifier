// Main JavaScript for image classifier functionality

document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const urlInput = document.getElementById('imageUrl');
    const urlPreview = document.getElementById('urlPreview');
    const previewImage = document.getElementById('previewImage');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Drag and drop functionality
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidImageFile(file)) {
                fileInput.files = files;
                updateDropZoneText(file.name);
            } else {
                showAlert('Please select a valid image file', 'error');
            }
        }
    });

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            updateDropZoneText(file.name);
        }
    });

    // URL preview functionality
    urlInput.addEventListener('input', function() {
        const url = this.value.trim();
        if (url && isValidImageUrl(url)) {
            showUrlPreview(url);
        } else {
            hideUrlPreview();
        }
    });

    // Form submission handlers
    uploadForm.addEventListener('submit', function(e) {
        const file = fileInput.files[0];
        if (!file) {
            e.preventDefault();
            showAlert('Please select a file', 'error');
            return;
        }
        
        if (!isValidImageFile(file)) {
            e.preventDefault();
            showAlert('Please select a valid image file', 'error');
            return;
        }

        showLoadingSpinner();
    });

    // URL form submission
    document.querySelector('form[action*="classify_url"]').addEventListener('submit', function(e) {
        const url = urlInput.value.trim();
        if (!url) {
            e.preventDefault();
            showAlert('Please enter a valid URL', 'error');
            return;
        }
        
        showLoadingSpinner();
    });

    // Helper functions
    function isValidImageFile(file) {
        const validTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp'];
        const maxSize = 16 * 1024 * 1024; // 16MB
        
        return validTypes.includes(file.type) && file.size <= maxSize;
    }

    function isValidImageUrl(url) {
        try {
            new URL(url);
            return /\.(jpg|jpeg|png|gif|bmp|webp)(\?.*)?$/i.test(url);
        } catch {
            return false;
        }
    }

    function updateDropZoneText(filename) {
        const content = dropZone.querySelector('.drop-zone-content');
        content.innerHTML = `
            <i class="fas fa-check-circle fa-3x mb-3 text-success"></i>
            <p class="mb-2">File selected: <strong>${filename}</strong></p>
            <p class="text-muted">Click to select a different file</p>
        `;
    }

    function showUrlPreview(url) {
        previewImage.src = url;
        previewImage.onerror = function() {
            hideUrlPreview();
            showAlert('Unable to load image from URL', 'warning');
        };
        previewImage.onload = function() {
            urlPreview.style.display = 'block';
        };
    }

    function hideUrlPreview() {
        urlPreview.style.display = 'none';
        previewImage.src = '';
    }

    function showLoadingSpinner() {
        loadingSpinner.style.display = 'block';
    }

    function hideLoadingSpinner() {
        loadingSpinner.style.display = 'none';
    }

    function showAlert(message, type) {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of container
        const container = document.querySelector('.container');
        const firstRow = container.querySelector('.row');
        container.insertBefore(alertDiv, firstRow);

        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Hide loading spinner on page load (in case of redirect)
    hideLoadingSpinner();

    // Auto-dismiss alerts after 10 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.querySelector('.btn-close')) {
                alert.remove();
            }
        });
    }, 10000);
});
