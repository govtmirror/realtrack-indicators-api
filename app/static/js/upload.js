$(document).on('change', '.btn-file :file', function() {
    var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselected', label);
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselected', function(event, label) {
        $('span[id="selected-file-name"]').text(label);
        $('span[id="selected-file-name"]').removeClass('hide');
    });
});
