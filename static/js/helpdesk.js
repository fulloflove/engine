$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
    $('.autosizeable').autosize();
    $('body').on('click','.contact_picker',function(){
        $('#contact_name').text($(this).text());
        $('#id_contact').val($(this).data('contact'));
        $('#clear_contact').removeClass('hidden');
        return false;
    });
    $('body').on('click','#clear_contact',function(){
        $('#contact_name').text('---------');
        $('#id_contact').val("");
        $(this).addClass('hidden');
        return false;
    });
    $('body').on('click','.clear_form',function(){
        resetForm($('#filter_form'));
        $('.errorlist').remove()
        return false;
    });
    $('body').on('click','.quick_edit',function(e){
        var block = $(this).data('block');
        $('.quick_edit_'+block).toggle();
        $('.quick_edit').toggle();
        var id_block = 'id_'+block;
        $('textarea[id^="' + id_block + '"]').autosize();
        e.preventDefault();
    });
    $('.quick_filter').on('change', function() {
        url = '/helpdesk/';
        url = url + $(this).attr("name") + '/' + $(this).val();
        window.location.replace(url);
    });
    $('#contact_form_modal').click( function(e) {
        var reg_id = $('#id_region').val();
        if(reg_id == "") {
            $('#choose_initiator').removeClass('hidden');
            $('#choose_initiator').show();
            $('#choose_initiator').fadeOut(3000);
        }
        else {
            console.log(reg_id);
            $('#choose_initiator').addClass('hidden');
            $('#modal_region').text($('#id_region option:selected').text());
            $('#newContact').modal('show');
        }
    });
});

$('.datepicker').datepicker({
    language: 'ru',
    format: 'dd.mm.yyyy',
    autoclose: true,
    todayHighlight: true,
})

$('a.popup-ajax').popover({
    "html": true,
    "trigger": "focus",
    "placement": "bottom",
    "container": "body",
    "content": function(){
        var div_id =  "tmp-id-" + $.now();
        return details_in_popup($(this).attr('data-target'), div_id);
    }
});

function details_in_popup(link, div_id){
    var reg_id = $('#id_region').val();
    var reg_link = link + reg_id;
    $.ajax({
        url: reg_link,
        success: function(response){
            $('#'+div_id).html(response);
        }
    });
    return '<div id="'+ div_id +'">'
        + '<div class="progress progress-striped active">'
        + '<div class="progress-bar" style="width:100%"></div>'
        + '</div></div>';
}

$("#ContactModal").on("show.bs.modal", function(e) {
    var link = $(e.relatedTarget);
    $(this).find(".modal-content").load(link.attr("href"));
});


function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}