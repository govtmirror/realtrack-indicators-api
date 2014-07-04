$(function() {
    $('select#country').change(function(){
        updateprojects($(this).val())
    });

    function updateprojects(country){
        $.post(
            '/updateprojects',
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
