var lastDate; //마지막 메세지 날짜(landing-chat)
var checkFirstChat; //첫번째 챗 판별

//landing-chat 채팅화면렌더링함수
function chatRender() {
    $.ajax({
        type: "GET",
        url: "/chat/",
        data: {"message": $('#chat-box').val()},
        success: function(res) {
            var e = $(res).find('#chat-box').children();
            $('#chat-box').children().remove();
            $('#chat-box').html(e);
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
        }
    });
}
//landing-chat db trigger
function dbTrigger() {
    $.ajax({
         type: "POST",
         url: "/chat/",
         beforeSend: function(xhr) {
             xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
         },
         data: {"dbtrigger": 1},
         success: function(res){
            if((lastDate<res.last_msg)&&(checkFirstChat==0)) {
                chatRender()
                lastDate = res.last_msg
            }
            else {
                lastDate = res.last_msg
                checkFirstChat=res.checkFirstChat
            }
         },
         error: function (res) {
             alert("dbTrigger 에러. 네트워크를 확인하세요")
         }
    });
}

$(document).ready(function(){
    //  LANDING-CHAT
    if (window.location.pathname==='/') {
        //엔터감지
        $('#landing-chat-input').keydown(function (key) {
            if (key.keyCode == 13) {
                $('#landing-chat-send').click();
            }
        });
        //최초렌더링
        chatRender();
        $('#landing-chat-send').on("click", (e) => {
            message = $('#landing-input-area').val();
            if (message.trim() != '') {
                $.ajax({
                    type: "POST",
                    url: '/chat/',
                    data: {"message": message, "dbtrigger": 0},
                    dataType: "json",
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                    },
                    success: function (res) {
                        chatRender();
                        setTimeout(function () {
                            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                        }, 100)
                        $('#landing-input-area').val('');
                    },
                    error: function (res) {
                        alert("전송실패. 지속될 경우 에러제보페이지에 문의바랍니다.")
                    }
                });
            }
        });
        //0.5초마다 db감시
        setInterval(dbTrigger, 500);
    }
});