
(function () {
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
                if(key.keyCode == 27) {
                    closeAll();
                }
            });
        };

        const closeAll = function() {
            let openModal = document.querySelectorAll('.' + elements.active);
            openModal.forEach(function (modal) {
                modal.classList.remove(elements.active);
            })
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
            document.getElementsByTagName('html')[0].style.overflow = "hidden"
            document.getElementsByTagName('body')[0].style.overflowY = "scroll";
        };

        const unFreeze = function () {
            document.getElementsByTagName('html')[0].style.overflow = ""
            document.getElementsByTagName('body')[0].style.overflowY = "";
        };

        return {
            init: function () {
                events();
            }
        }
    })();



    window.onload = function(e){
        // Initialize modal windows
        modalFX.init();

        let timer = 0.3,
            $modals = document.querySelector('.save-the-date.modal');

        setTimeout(function() {
            $modals.classList.add('is-active');
        }, timer * 1000);

    };

})();
