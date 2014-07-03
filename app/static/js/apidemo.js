$(function() {
    $('select#country').off('click').on('click', function(){
        updateprojects($(this).val())
    });

    function updateprojects(country){
        $.post(
            $SCRIPT_ROOT + '/updateprojects',
            {'country': country},
            function(data) {
                        /* update project when country changes */
                        $('select#project').empty();
                        $.each(data["options"], function(i, value) {
                            $('select#project').append($('<option>').text(value).attr('value', value));
                        });
                     },
            'json'
        );
        return false;
    };

});
