"use strict";


const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const wallpapersAjaxRoute = document.querySelector('meta[name="wallpapers-ajax-route"]').getAttribute('content');


var tooltipTriggerList;
var tooltipList;
var imgLoad;
var msnry;
var viewer;



(function () {
    document.body.addEventListener('htmx:configRequest', function (event) {
        if (token) {
            event.detail.headers['X-CSRFToken'] = token;
        }
    });


    document.body.addEventListener('htmx:load', function (event) {
        showMessages();
        initTooltip();
        initViewer();
    });


    document.addEventListener('alpine:init', () => {
        Alpine.data(
            'filters',
            function () {
                return {
                    category: this.$persist('').using(sessionStorage),
                    orientation: this.$persist('').using(sessionStorage),
                    fetchWallpapers() {
                        htmx.ajax(
                            'GET',
                            `${wallpapersAjaxRoute}?${new URLSearchParams({ category: this.category, orientation: this.orientation })}`,
                            '#wallpapers',
                        );
                    },
                    init() {
                        // keep all state in sync
                        let optionNotFound = true;
                        for(const option of this.$refs.category_filter.options) {
                            if(this.category === option.value) {
                                optionNotFound = false;
                            }
                        }
                        if(optionNotFound === true) {
                            this.category = this.$refs.category_filter.value;
                        }

                        optionNotFound = true;
                        for(const option of this.$refs.orientation_filter.options) {
                            if(this.orientation === option.value) {
                                optionNotFound = false;
                            }
                        }
                        if(optionNotFound === true) {
                            this.orientation = this.$refs.orientation_filter.value;
                        }
                    }
                };
            }
        );
    });
})();


/**
 * Initializes bootstrap tooltip.
 */
function initTooltip() {
    tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el));
}


/**
 * Show toasts for all loaded messages.
 */
function showMessages() {
    loadMessages().forEach(message => {
        showToast(message);
    });
}


/**
 * Retrieves an array of messages from paragraph elements inside the div with id "messages" and removes them.
 * @returns {Array<string>} - The array of messages
 */
function loadMessages() {
    let array_to_return = Array.from(document.querySelectorAll('#messages > p'))
        .map(el => el.textContent ?? '');

    document.querySelectorAll('#messages > p').forEach(p => p.remove());
    return array_to_return;
}


/**
 * Invokes the Bootstrap toast with the given message
 * @param {string} message - The message to toast
 */
function showToast(message) {
    let toastContainer = document.querySelector('.toast-container');

    // Create a div and set innerHTML to generate the toast structure
    let wrapper = document.createElement('div');
    wrapper.innerHTML = `
            <div class="toast rounded-0 bg-success mb-2" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-body d-flex flex-row justify-content-between">
                    <div class="text-white fw-bold">${message}</div>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close">
                    </button>
                </div>
            </div>
        `;

    let toastEl = wrapper.firstElementChild;
    toastContainer.appendChild(toastEl);

    let toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}


/**
* Initialize the Viewer.
* @param {HTMLElement} element - The image element passed to viewer
*/
function initViewer() {
    let imgEl = document.getElementById("wallpaper-image-view")
    if (imgEl !== null) {
        viewer = new Viewer(
            imgEl,
            {
                toolbar: {
                    play: true,
                },
                navbar: false,
                title: false,
            }
        )
    }
}


/**
 * Initializes masonry and imagesLoaded for .grid component.
 */
function loadGrid() {
    imgLoad = imagesLoaded(document.querySelector('.grid'));

    msnry = new Masonry(document.querySelector('.grid'), {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: '.gutter-sizer',
    });

    imgLoad.on('progress', function (instance, image) {
        msnry.layout()
        if (image.isLoaded === true) {
            image.img.parentNode.classList.remove('loading-item');
        }
    });

    imgLoad.on('always', function (instance) {
        var button = document.querySelector('#load-more-button-container > button');
        if (button !== null && button.hasAttribute('disabled')) {
            button.removeAttribute('disabled');
        }
    });
}
