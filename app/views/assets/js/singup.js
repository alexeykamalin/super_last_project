
(function ($) {
    "use strict";
    /*==================================================================
    [ Validate ]*/

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

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
        $('.validate-form .input100').each(function(){
            if (validate($(this)) == false){
                showValidate($(this));
                check = false;
            }
            if($('#pass_user').val() != $('#pass_user_2').val()){
                showValidate($('#pass_user'));
                showValidate($('#pass_user_2'));
                check = false;
            }
        });
        return check
    }
    
    /*==================================================================
    [ Show pass ]*/
    var showPass = 0;
    $('.btn-show-pass').on('click', function(){
        if(showPass == 0) {
            $(this).next('input').attr('type','text');
            $(this).find('i').removeClass('fa-eye');
            $(this).find('i').addClass('fa-eye-slash');
            showPass = 1;
        }
        else {
            $(this).next('input').attr('type','password');
            $(this).find('i').removeClass('fa-eye-slash');
            $(this).find('i').addClass('fa-eye');
            showPass = 0;
        } 
    });
    $('#registration').on('click', function(e){
        e.preventDefault();
        if(Validation()){
            $.ajax({
                contentType: 'application/json',
                url: 'api/users/signup',
                type: 'POST',
                data: JSON.stringify({
                    email: $('#email_user').val(),
                    password: $('#pass_user').val(),
                    name: $('#name_user').val(),
                })
            }).done(function(data){
                console.log(data);
                if(data.result=='true'){
                    window.location.href = '/';
                }else{
                    $('#email_user').parent().attr('data-validate','Такой пользователь уже есть')
                    showValidate($('#email_user'))
                }
            });
        }
    })
})(jQuery);
