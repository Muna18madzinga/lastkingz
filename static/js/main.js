// LastKings POS - Main JavaScript

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });
});

// Update status info
function updateStatus(message) {
    const statusInfo = document.getElementById('statusInfo');
    if (statusInfo) {
        statusInfo.textContent = message;
    }
}

// Message Box System
let messageBoxOverlay = null;

function createMessageBoxOverlay() {
    if (!messageBoxOverlay) {
        messageBoxOverlay = document.createElement('div');
        messageBoxOverlay.className = 'message-box-overlay';
        messageBoxOverlay.addEventListener('click', function(e) {
            if (e.target === messageBoxOverlay) {
                closeMessageBox();
            }
        });
        document.body.appendChild(messageBoxOverlay);
    }
    return messageBoxOverlay;
}

function showMessageBox(options) {
    const overlay = createMessageBoxOverlay();

    const type = options.type || 'info'; // success, error, warning, info
    const title = options.title || 'Message';
    const message = options.message || '';
    const buttons = options.buttons || [{text: 'OK', primary: true, callback: closeMessageBox}];

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    const messageBox = document.createElement('div');
    messageBox.className = `message-box ${type}`;

    // Header
    const header = document.createElement('div');
    header.className = 'message-box-header';
    header.innerHTML = `
        <div class="message-box-icon">${icons[type]}</div>
        <h3 class="message-box-title">${title}</h3>
    `;

    // Body
    const body = document.createElement('div');
    body.className = 'message-box-body';
    body.innerHTML = message;

    // Footer
    const footer = document.createElement('div');
    footer.className = 'message-box-footer';

    buttons.forEach(btn => {
        const button = document.createElement('button');
        button.className = btn.primary ? 'btn btn-primary' : 'btn btn-secondary';
        button.textContent = btn.text;
        button.onclick = function() {
            if (btn.callback) {
                btn.callback();
            }
            closeMessageBox();
        };
        footer.appendChild(button);
    });

    messageBox.appendChild(header);
    messageBox.appendChild(body);
    messageBox.appendChild(footer);

    overlay.innerHTML = '';
    overlay.appendChild(messageBox);
    overlay.style.display = 'flex';

    // Focus first button
    setTimeout(() => {
        const firstBtn = footer.querySelector('button');
        if (firstBtn) firstBtn.focus();
    }, 100);
}

function closeMessageBox() {
    if (messageBoxOverlay) {
        messageBoxOverlay.style.display = 'none';
        messageBoxOverlay.innerHTML = '';
    }
}

// Convenience functions
function showSuccess(message, title = 'Success') {
    showMessageBox({
        type: 'success',
        title: title,
        message: message
    });
}

function showError(message, title = 'Error') {
    showMessageBox({
        type: 'error',
        title: title,
        message: message
    });
}

function showWarning(message, title = 'Warning') {
    showMessageBox({
        type: 'warning',
        title: title,
        message: message
    });
}

function showInfo(message, title = 'Information') {
    showMessageBox({
        type: 'info',
        title: title,
        message: message
    });
}

function showConfirm(message, title, onConfirm, onCancel) {
    showMessageBox({
        type: 'warning',
        title: title || 'Confirm',
        message: message,
        buttons: [
            {
                text: 'Cancel',
                primary: false,
                callback: onCancel || function() {}
            },
            {
                text: 'Confirm',
                primary: true,
                callback: onConfirm || function() {}
            }
        ]
    });
}
