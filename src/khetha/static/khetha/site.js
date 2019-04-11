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

  // https://material.io/develop/web/components/input-controls/radio-buttons/#javascript-instantiation
  [].map.call(document.querySelectorAll(".mdc-radio"), function(radioButtonEl) {
    if (radioButtonEl.MDCRadio) {
      var formFieldQuery = $(radioButtonEl).closest(".mdc-form-field");
      formFieldQuery.each(function(index, formFieldEl) {
        if (formFieldEl.MDCFormField) {
          // Associate the radio component with its form-field component
          formFieldEl.MDCFormField.input = radioButtonEl.MDCRadio;
        } else {
          console.log("Warning, MDCFormField not initialised on:", formFieldEl);
        }
      });
    } else {
      console.log("Warning, MDCRadio not initialised on:", radioButtonEl);
    }
  });

  // Initialise and open any progress bars marked with data-khetha-initial-progress.
  // https://material.io/develop/web/components/linear-progress/
  [].map.call(document.querySelectorAll(".mdc-linear-progress"), function(el) {
    if (el.dataset.khethaInitialProgress) {
      if (el.MDCLinearProgress) {
        el.MDCLinearProgress.progress = el.dataset.khethaInitialProgress;
        el.MDCLinearProgress.open();
      } else {
        console.log("Warning, MDCLinearProgress not initialised:", el);
      }
    }
  });

  // Dialog handling.
  // https://material.io/develop/web/components/dialogs/
  [].map.call(document.querySelectorAll(".mdc-dialog"), function(el) {
    /** @type {MDCDialog} */
    var dialog = el.MDCDialog;
    if (dialog) {
      // Handle data-khetha-dialog-auto-open
      if (el.dataset.khethaDialogAutoOpen === "once") {
        dialog.open();
        el.dataset.khethaDialogAutoOpen = "opened";
      }

      // Handle data-khetha-dialog-behaviour
      if (el.dataset.khethaDialogBehaviour === "task-complete") {
        dialog.listen("MDCDialog:closed", function(event) {
          /** @type {string} */
          var action = event.detail.action;
          if (action === "continue") {
            document.location = "/";
          }
          // Otherwise, assume "close"
        });
      }
    } else {
      console.warn("MDCDialog not initialised on", el);
    }
  });
}

// Guard variable: Google Maps API loaded yet?
var isGoogleMapsLoaded = false;

function initGoogleMapsAutocomplete() {
  if (isGoogleMapsLoaded) {
    var elements = document.querySelectorAll(".google-maps-autocomplete");
    [].map.call(elements, function(el) {
      new google.maps.places.Autocomplete(el);
    });
  }
  // Just skip if not ready yet: a later call should get it.
}
function setGoogleMapsLoaded() {
  isGoogleMapsLoaded = true;
  initGoogleMapsAutocomplete();
}

function initWidgets() {
  initMDC();
  initGoogleMapsAutocomplete();

  // http://www.jacklmoore.com/autosize/
  autosize(document.querySelectorAll(".textarea--autosize"));
}

initWidgets();

// Enable the question cards' khetha-collapsible toggles.
$(".khetha-card--question-complete .mdc-card__primary-action").live(
  "click keypress",
  function(event) {
    var $collapsible = $(event.target)
      .closest(".khetha-card--question-complete")
      .find(".khetha-collapsible");
    $collapsible.toggleClass("khetha-collapsible--collapsed");
  }
);
