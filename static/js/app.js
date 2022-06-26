$(document).ready(function(){
            $(".select2_el").select2({
            });
        });

$(document).ready(function () {
        //Toggle fullscreen
        $(".chat-bot-icon").click(function (e) {
            $(this).children('img').toggleClass('hide');
            $(this).children('svg').toggleClass('animate');
            $('.chat-screen').toggleClass('show-chat');
        });
        // $('.chat-mail button').click(function () {
            
        // });
        $('.end-chat').click(function () {
            $('.chat-body').addClass('hide');
            $('.chat-input').addClass('hide');
            $('.chat-session-end').removeClass('hide');
            $('.chat-header-option').addClass('hide');
        });
    });

    $(document).ready(function() {
        $('#todo-form').on('submit', function(event) {
          $.ajax({
             data : {
                msg : $('#todo').val(), 
               },
                type : 'POST',
                url : '/request'
           })
           .done(function(data){
               var result = data.answer;
              if(result.indexOf("http") > -1 || result.indexOf("https") > -1){
               $('#answer').append('<div class="chat-bubble me">'+$('#todo').val()+'</div>' +  '<a href=' + data.answer +'class="chat-bubble you" target="_blank">'+data.answer+'</a>');
               $('#todo').val('');
              }else{
               $('#answer').append('<div class="chat-bubble me">'+$('#todo').val()+'</div>' +  '<div class="chat-bubble you">'+data.answer+'</div>');
               $('#todo').val('');
              }
         });
         event.preventDefault();
         });
   });
   $(document).ready(function() {
    $('#submit_email').on('submit', function(event) {
      $.ajax({
         data : {
            email : $('#email').val(), 
           },
            type : 'POST',
            url : '/submit_email'
       })
       .done(function(data){
        let ele = document.getElementById('alert');
        ele.innerHTML = '';
          if(data.status == ""){
            $('.chat-mail').addClass('hide');
            $('.chat-body').removeClass('hide');
            $('.chat-input').removeClass('hide');
            $('.chat-header-option').removeClass('hide');
          }
          if(data.status != ""){
            ele.innerHTML = "Invalid email address!";
          }
     });
     event.preventDefault();
    });
     });

     var rate;
     $("#great").click(function() {
        rate = 1;
        alert(rate);
    });

    $("#bad").click(function() {
        rate = 2;
        alert(rate);
    });

     $(document).ready(function() {
        $('#rate').on('submit', function(event) {
          $.ajax({
            type: "POST",
    url: "/rate",
    contentType: "application/json",
    data: JSON.stringify({r: rate}),
    dataType: "json",
    success: function(response) {
        console.log(response);
    },
    error: function(err) {
        console.log(err);
    }
         });
         event.preventDefault();
         });
   });
   