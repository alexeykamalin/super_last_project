
(function ($) {
    "use strict";
    /*==================================================================
    [ Validate ]*/
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
          window.location.reload();
        }
      });
    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    function Validation() {
        var check = true;
        
        return check
    }
    /*==================================================================
    [ Validate ]*/
    $('#add_balance').on('click', function(){
        if($('#tugrik').val() > 100000){
            $('.main_body').html('Нельзя пополнить больше, чем на 100000,<br/>Введите количество средств для пополнения <input id="tugrik"/>')
        }else{
            if(Validation()){
                $.ajax({
                    contentType: 'application/json',
                    url: '/api/balance/update_balance',
                    type: 'POST',
                    data: JSON.stringify({
                        value: $('#tugrik').val(),
                        user_id: $('#options').attr('user_id'),
                    })
                }).done(function(data){
                    console.log(data);
                    if(data.result){
                        window.location.href = '/';
                    }
                });
            }
        }
            
    })

    $('.delete_user').on('click', function(){
        $('#delete_user').attr('data_user', $(this).attr('id'))
        $('.modal-body').html("<div class='row'><div class='col-lg-12 col-sm-12 alert alert-primary'>Вы уверены, что хотите удалить</div></div>").append($(this).attr('name'));
    })

    $('#delete_user').on('click', function(){
        $.ajax({
            contentType: 'application/json',
            url: '/api/users/delete_user',
            type: 'POST',
            data: JSON.stringify({
                user_id: $(this).attr('data_user').split('_')[1],
            })
        }).done(function(data){
            console.log(data);
            if(data.result){
                window.location.href = '/';
            }
        });
    })
    
})(jQuery);
