"use strict";

import { Toast } from "../vendor/bootstrap.mjs";


/**
 * Retrieves string constants from HTML elements whose IDs start with "constant-" and end with the specified name suffix.
 * @param {string} name The id suffix
 * @returns {string} The constant value, or an empty string if the element is not found or has no text content.
 */
export function loadConstant(name) {
    const el = document.getElementById(`constant-${name}`);
    return el?.textContent ?? '';
}


/**
 * Retrieves an array of messages from paragraph elements inside the div with id "messages".
 * @returns {Array<string>} - The array of messages
 */
export function loadMessages() {
    return Array.from(document.querySelectorAll('#messages > p'))
                .map(el => el.textContent ?? '');
}


/**
 * Invokes the bootstrap toast with the given message
 * @param {string} message - The message to toast
 * @returns {void}
 */
export function showToast(message) {
    const container = document.getElementById('toastContainer');

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-white bg-success border-0 mb-2';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
<div class="d-flex">
<div class="toast-body fw-bold">${message}</div>
<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
</div>
`;

    container.appendChild(toastEl);
    const toast = new Toast(toastEl, { delay: 3000 });
    toast.show();

    // Remove from DOM after hidden
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}
