$(document).ready(function(){  
    $('form').on("submit", function(event) {
        $.ajax({
            data : {
                selected_destination: $('#selected_destination').val()
            },
            type: 'POST',
            url: '/'
        })
        .done(function(data){
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else {
                $('#errorAlert').hide();
                $('#successAlert').text(data.name).show();
            }
        })
    event.preventDefault();
    });

});
