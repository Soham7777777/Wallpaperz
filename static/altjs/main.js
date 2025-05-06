"use strict";

import { htmx } from "./vendor/htmx.mjs";

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
