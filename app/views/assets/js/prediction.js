
(function ($) {
    "use strict";
    if ($('body:contains("in_progress")').length) {
        setInterval(() => {
            window.location.reload();
        }, 10000);
    }
    
    /*==================================================================
    [ Validate ]*/

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function isImageUrlByExtension(url) {
        const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
        const lowerUrl = url.toLowerCase();
        return imageExtensions.some(ext => lowerUrl.endsWith(ext));
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
        
        return check
    }
    /*==================================================================
    [ Validate ]*/
    $('#get_prediction').on('click', function(){
        if(isImageUrlByExtension($('#prediction_text').val())){
            if(Validation()){
                $.ajax({
                    contentType: 'application/json',
                    url: '/api/prediction/create_prediction',
                    type: 'POST',
                    data: JSON.stringify({
                        user_id: Number($('#options').attr('user_id')),
                        image: $('#prediction_text').val(),
                    })
                }).done(function(data){
                    console.log(data);
                    if(data.result == 'true'){
                        window.location.href = '/predictions';
                    }else if(data.result == 'false' && data.message == 'no limits'){
                        $('.modal-body').html('<div class="row"><div class="col-lg-12 col-sm-12 alert alert-primary">Упс, кажется у Вас кончились средства. <a href="/">Пополнить?</a></div></div>')
                    }
                });
            }
        }else{
            $('.main_body').html('Не правильная ссылка на изображение.<br/>Введите ссылку на картику, на которой необходимо определить: есть ли машина?<input id="prediction_text" style="margin: 20px; width: 400px; padding: 10px;">')
        }
        
    })
    
})(jQuery);
