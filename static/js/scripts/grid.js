"use strict";

var imgLoad;
var msnry;


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
