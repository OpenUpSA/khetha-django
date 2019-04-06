/* Site-wide initialisation for Khetha. */

(function () {
    // https://material.io/develop/web/components/top-app-bar/#javascript-instantiation
    const topAppBar = new window.mdc.topAppBar.MDCTopAppBar(document.querySelector('.mdc-top-app-bar'));

    //https://material.io/develop/web/components/input-controls/text-field/#javascript-instantiation
    const textFields= [].map.call(document.querySelectorAll('.mdc-text-field'), function (el) {
        return new window.mdc.textfield.MDCTextField(el);
    });

    // https://material.io/develop/web/components/cards/#javascript
    const selector = '.mdc-button, .mdc-icon-button, .mdc-card__primary-action';
    const ripples = [].map.call(document.querySelectorAll(selector), function (el) {
        return new window.mdc.ripple.MDCRipple(el);
    });

    // https://material.io/develop/web/components/snackbars/#javascript-instantiation
    const snackbars = [].map.call(document.querySelectorAll('.mdc-snackbar'), function (el) {
        console.log(el);
        let snackbar = new window.mdc.snackbar.MDCSnackbar(el);
        // The Django messages snackbars should open on page load.
        snackbar.open();
        return snackbar;
    });


})();
