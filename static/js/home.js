var grid = document.querySelector('.grid');
var msnry;


function masonryInit() {
    msnry = new Masonry(grid, {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: '.gutter-sizer',
    });

    imagesLoaded(grid).on('progress', function (instance, image) {
        msnry.layout();
        if (image.isLoaded === true) {
            image.img.parentNode.classList.remove('loading-item');
        }
    });

    imagesLoaded(grid).on('always', function (instance) {
        const button = document.querySelector('#load-more-button-container > button');
        if (button !== null && button.hasAttribute('disabled')) {
            button.removeAttribute('disabled');
        }
    });
}

(function () {
    "use strict";

    htmx.ajax(
        "GET",
        ajax_wallpaper_url,
        {
            target: "#wallpapers",
            swap: "beforeend",
        }
    ).then(() => {
        masonryInit();
    });

    htmx.onLoad(function (elt) {
        masonryInit();
    });

}());
