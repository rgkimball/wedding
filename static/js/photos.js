"use strict";


(function (window, undefined) {
    const gallery = (function () {

        const elements = {
            items: '.grid-item',
            container: '.grid'
        };

        const onClickEach = function (selector, callback) {
            let arr = document.querySelectorAll(selector);
            arr.forEach(function (el) {
                el.addEventListener('click', callback, el);
            })
        };

        const events = function() {
            onClickEach(elements.items, enlarge)
        };

        const enlarge = function(tgt, test) {
            let $all = document.querySelectorAll(elements.items),
                $this = tgt.toElement,
                $body = document.querySelector('body');

            Array.prototype.forEach.call($all, function($e) {
                $e.classList.remove('enlarged')
            });
            // Toggle
            if ($this.parentElement.classList.contains('enlarged')) {
                $this.parentElement.classList.remove('enlarged');
            } else {
                $this.parentElement.classList.add('enlarged');
            }
        };

        return {
            init: function () {
                events();
            }
        }
    })();

    if (!window.hasOwnProperty('load_functions')) {
        window.load_functions = Array();
    }

    window.load_functions.push(function(){

        gallery.init()

    });

})(window, undefined);

