/**
 * Replace a form element from new page data.
 *
 * @param {HTMLFormElement} form
 * @param {string} newPageData
 */
function replaceForm(form, newPageData) {
  var formAnchor = "#" + form.id;
  var fresh = $(formAnchor, newPageData);
  $(formAnchor).replaceWith(fresh);

  // Restore the submit button / hidden input hack after replacement.
  $(formAnchor).append('<div class="submit-button-hidden-input-hack">');

  // Reinitialise any new widgets that need JavaScript.
  initWidgets();
}

/**
 * Submit and replace a form in-place, asynchronously.
 *
 * @param {Event} e
 */
function inplaceSubmit(e) {
  /**
   * @param {string} data
   * @param {string} status
   * @param {XMLHttpRequest} xhr
   * */
  function handleResponse(data, status, xhr) {
    if (document.URL === xhr.responseURL) {
      replaceForm(form, data);
    } else {
      // If the response URL differs, treat it as a redirect.
      document.location = xhr.responseURL;
    }
  }

  e.preventDefault();
  /** @type {HTMLFormElement} */
  var form = e.target;
  $.post(form.action, $(form).serializeArray(), handleResponse);
}

// This works around the issue of submit buttons not being reliably available
// to serializeArray, FormData, and such.
function submitButtonHiddenInputHack() {
  $(this.form)
    .find(".submit-button-hidden-input-hack")
    .html($("<input type=hidden>").attr({ name: "value", value: this.value }));
}

$(document).ready(function() {
  var $form = $(".inplace-submit-form");
  $form.live("submit", inplaceSubmit);
  // Enable the submit button / hidden input hack.
  $form.append('<div class="submit-button-hidden-input-hack">');
  $(".trigger-submit-button-hidden-input-hack").live(
    "click",
    submitButtonHiddenInputHack
  );
});
