"use strict";


(function (window) {

    const headerNav = (function() {

        const elements = {
            $body: document.querySelector('body'),
            $button: document.querySelector('h1.stamp .amp'),
            $nav: document.querySelector('nav'),
            $navTrigger: document.querySelector('#nav-button'),
        };

        return {
            init: function() {

                elements.$button.onclick = function($this) {
                    if (!elements.$body.classList.contains('homepage')) {
                        // Toggler
                        if (!elements.$nav.classList.contains('active')) {
                            elements.$nav.classList.add('active');
                        } else {
                            elements.$nav.classList.remove('active');
                        }
                    }

                };

                elements.$navTrigger.onclick = function($this) {
                    if (elements.$nav.classList.contains('is-active')) {
                        // Toggle off
                        elements.$navTrigger.classList.remove('is-active');
                        elements.$nav.classList.remove('is-active');
                    } else {
                        // Toggle on
                        elements.$navTrigger.classList.add('is-active');
                        elements.$nav.classList.add('is-active');
                    }
                }

            }
        };

    })();

    const modalFX = (function () {

        const elements = {
            target: 'data-target',
            active: 'is-active',
            button: '.modal-button',
            close: '.modal-close',
            buttonClose: '.modal-button-close',
            background: '.modal-background'
        };

        const onClickEach = function (selector, callback) {
            let arr = document.querySelectorAll(selector);
            arr.forEach(function (el) {
                el.addEventListener('click', callback);
            })
        };

        const events = function () {
            onClickEach(elements.button, openModal);

            onClickEach(elements.close, closeModal);
            onClickEach(elements.buttonClose, closeAll);
            onClickEach(elements.background, closeModal);

            // Close all modals if ESC key is pressed
            document.addEventListener('keyup', function(key){
                if(key.keyCode === 27) {
                    closeAll();
                }
            });
        };

        const closeAll = function() {
            let openModal = document.querySelectorAll('.' + elements.active);
            openModal.forEach(function (modal) {
                modal.classList.remove(elements.active);
            });
            unFreeze();
        };

        const openModal = function () {
            let modal = this.getAttribute(elements.target);
            freeze();
            document.getElementById(modal).classList.add(elements.active);
        };

        const closeModal = function () {
            let modal = this.parentElement.id;
            document.getElementById(modal).classList.remove(elements.active);
            unFreeze();
        };

        // Freeze scrollbars
        const freeze = function () {
            document.getElementsByTagName('html')[0].style.overflow = "hidden";
            document.getElementsByTagName('body')[0].style.overflowY = "scroll";
        };

        const unFreeze = function () {
            document.getElementsByTagName('html')[0].style.overflow = "";
            document.getElementsByTagName('body')[0].style.overflowY = "";
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

        // Initialize nav
        headerNav.init();

        // Initialize modal windows
        modalFX.init();

        let $modals = document.querySelectorAll('.save-the-date.modal');

        // hack.
        window.NodeList.prototype.reverse = Array.prototype.reverse;

        $modals.forEach(function($m, index) {
            setTimeout(function(){
                $m.classList.add('is-active');
            }, 350 * (index + 1));
        });



    });

    /**
     * getJSON()
     *
     * Use the callback function to get a return.
     *
     * @param url string, valid URI
     * @param callback function
     */
    window.getJSON = function(url, callback) {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';

        xhr.onload = function() {
            let status = xhr.status;
            if (status === 200) {
                callback(xhr.response);
            } else {
                throw Error("JSON Request of " + url + " failed. Status: " + status)
            }
        };
        xhr.send();
        return xhr.response;
    };

    // Call each
    window.onload = function() {

        window.load_functions.forEach(function(fn) {
            fn()
        });

    };

})(window);
