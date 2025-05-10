"use strict";

var viewer;


/**
 * Initialize the Viewer.
 * @param {HTMLElement} element - The image element passed to viewer
 */
function initViewer(element) {
    viewer = new Viewer(
        document.getElementById("wallpaper-image-view"),
        {
            toolbar: {
                play: true,
            },
            navbar: false,
            title: false,
        }
    )    
}


function previewFullscreen() {
    viewer.play(true);
}


document.body.addEventListener('htmx:afterSettle', function (event) {
    let imgEl = document.getElementById("wallpaper-image-view")
    if(imgEl !== null)
        initViewer(imgEl);
});

initViewer();
