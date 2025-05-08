"use strict";

import { Tooltip, Collapse } from "./vendor/bootstrap.mjs";
import { showToast, loadMessages } from "./modules/common.mjs";

var tooltipTriggerList;
var tooltipList;

var collapseElementList;
var collapseList;

document.body.addEventListener('htmx:configRequest', (event) => {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    if (token) {
        event.detail.headers['X-CSRFToken'] = token;
    }
});

function baseScript() {
    loadMessages().forEach(message => {
        showToast(message);
    });

    tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipList = [...tooltipTriggerList].map(el => new Tooltip(el));
}

baseScript();

document.body.addEventListener('htmx:afterSettle', function (event) {
    baseScript();
});
