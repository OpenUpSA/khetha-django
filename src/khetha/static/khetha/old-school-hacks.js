function inplaceSubmit(e) {
  e.preventDefault();
  var form = e.target;
  $.post(form.action, $(form).serializeArray(), function(response) {
    var formAnchor = "#" + form.id;
    var fresh = $(formAnchor, response);
    $(formAnchor).replaceWith(fresh);

    // Restore the submit button / hidden input hack after replacement.
    $(formAnchor).append('<div class="submit-button-hidden-input-hack">');

    // Reinitialise any new widgets that need JavaScript.
    initWidgets();
  });
}

// This works around the issue of submit buttons not being reliably available
// to serializeArray, FormData, and such.
function submitButtonHiddenInputHack() {
  $(this.form)
    .find(".submit-button-hidden-input-hack")
    .html($("<input type=hidden>").attr({ name: "value", value: this.value }));
}

$(document).ready(function() {
  $(".khetha-question-answer-form").live("submit", inplaceSubmit);

  // Enable the submit button / hidden input hack.
  $(".khetha-question-answer-form").append(
    '<div class="submit-button-hidden-input-hack">'
  );
  $(".trigger-submit-button-hidden-input-hack").live(
    "click",
    submitButtonHiddenInputHack
  );
});
