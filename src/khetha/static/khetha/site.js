/* Site-wide initialisation for Khetha. */

function initMDC() {
  // https://material.io/develop/web/components/auto-init/
  window.mdc.autoInit(
    document,
    // This initialisation gets called more than once per page load,
    // so don't warn for already-initialised components.
    function() {}
  );

  // https://material.io/develop/web/components/snackbars/#javascript-instantiation
  [].map.call(document.querySelectorAll(".mdc-snackbar"), function(el) {
    if (el.MDCSnackbar) {
      el.MDCSnackbar.open();
    } else {
      console.log("Warning, MDCSnackbar not initialised:", el);
    }
  });
}

initMDC();
