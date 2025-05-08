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
    let array_to_return = Array.from(document.querySelectorAll('#messages > p'))
                .map(el => el.textContent ?? '');
    document.querySelectorAll('#messages > p').forEach(p => p.remove());
    return array_to_return;
}


/**
 * Invokes the Bootstrap toast with the given message
 * @param {string} message - The message to toast
 * @returns {void}
 */
export function showToast(message) {
    const container = document.querySelector('.toast-container');

    // Create a div and set innerHTML to generate the toast structure
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="toast rounded-0 bg-success mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-body d-flex flex-row justify-content-between">
                <div class="text-white fw-bold">${message}</div>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close">
                </button>
            </div>
        </div>
    `;

    const toastEl = wrapper.firstElementChild;
    container.appendChild(toastEl);

    const toast = new Toast(toastEl, { delay: 3000 });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}