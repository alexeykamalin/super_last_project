
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

    $('#get_prediction').on('click', function(){
        $.ajax({
            contentType: 'application/json',
            url: '/api/prediction/create_prediction',
            type: 'POST',
            data: JSON.stringify({
                user_id: Number($('#options').attr('user_id')),
                a1: $('#a1').val(),
                a2: $('#a2').val(),
                a3: $('#a3').val(),
                ag: $('#ag').val(),
                g1: $('#g1').val(),
                g2: $('#g2').val(), 
                g3: $('#g3').val(),
                gg: $('#gg').val(),
                i1: $('#i1').val(),
                i2: $('#i2').val(),
                i3: $('#i3').val(),
                ia: $('#ia').val(),
                ig: $('#ig').val(),
                f1: $('#f1').val(),
                f2: $('#f2').val(),
                f3: $('#f3').val(),
                fa: $('#fa').val(),
                fg: $('#fg').val(),
                r1: $('#r1').val(),
                r2: $('#r2').val(),
                r3: $('#r3').val(), 
                ra: $('#ra').val(),
                rg: $('#rg').val(),
                pri: $('#pri').val(),
                prm: $('#prm').val(),
                prr: $('#prr').val(),
                prf: $('#prf').val(),
                egkr: $('#egkr').val(),
            })
        }).done(function(data){
            console.log(data);
            if(data.result == 'true'){
                window.location.href = '/predictions';
            }else if(data.result == 'false'){
                $('.main_body').html('Ошибка при создании предсказания, проверьте правильность введенных данных');
            }
        });
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
