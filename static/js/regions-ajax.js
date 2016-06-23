$(document).ready(function() {
    $('#suggestion').keyup(function() {
        var query = $(this).val();
        $.get('/regions/suggest_region/', {suggestion: query}, function(data) {
                $('#suggest_region').html(data);
        });
    });
});