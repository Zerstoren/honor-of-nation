define('libs/scrolling-disable', [], function () {
    // left: 37, up: 38, right: 39, down: 40,
    // spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
    var keys = [];

    function preventDefault(e) {
        e = e || window.event;
        var target = jQuery(e.target);

        if (target.hasClass('scrolling') || target.parents('.scrolling').length) {
            return true;
        }

        if (e.preventDefault) {
            e.preventDefault();
        }

        e.returnValue = false;
    }

    function keydown(e) {
        for (var i = keys.length; i--;) {
            if (e.keyCode === keys[i]) {
                preventDefault(e);
                return;
            }
        }
    }

    function wheel(e) {
        preventDefault(e);
    }

    function disable_scroll() {
        if (window.addEventListener) {
            window.addEventListener('DOMMouseScroll', wheel, false);
        }
        window.onmousewheel = document.onmousewheel = wheel;
        document.onkeydown = keydown;
    }

    function enable_scroll() {
        if (window.removeEventListener) {
            window.removeEventListener('DOMMouseScroll', wheel, false);
        }
        window.onmousewheel = document.onmousewheel = document.onkeydown = null;
    }

    disable_scroll();

    return {
        disable_scroll: disable_scroll,
        enable_scroll: enable_scroll
    };
});

require(['libs/scrolling-disable']);