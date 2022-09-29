
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//notification functions (show_notifications.html & contest_notify.html에서 onclick 확인)
// 댓글 알림 제거 & user_has_seen 체크
function removeNotification(removeNotificationURL, redirectURL) {
	const csrftoken = getCookie('csrftoken');
	let xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status == 200) {
				window.location.replace(redirectURL);
			} else {
				alert('알수없는 에러(1)가 발생했습니다. 지속된다면 to.devdreamer@gmail.com로 문의해주세요.');
			}
		}
	};

	xmlhttp.open("DELETE", removeNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}

function checkNotification(checkNotificationURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status != 200) {
				alert('알수없는 에러(2)가 발생했습니다. 지속된다면 to.devdreamer@gmail.com로 문의해주세요.');
			}
		}
	};

	xmlhttp.open("POST", checkNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}

//대회 및 공모전 알림 user_has_seen 체크
function manageNotification(checkNotificationURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status != 200) {
				alert('알수없는 에러(3)가 발생했습니다. 지속된다면 to.devdreamer@gmail.com로 문의해주세요.');
			}
		}
	};

	xmlhttp.open("DELETE", checkNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}



$(document).ready(function(){
    //대회 및 공모전 알림 user_has_seen 체크 작동
    if (window.location.pathname==='/contest/') {
        manageNotification(checkNotificationURL);
    }

    //알림 숫자 0으로 강제변경
    $("#noti-box").on("click", function(e){
       $.ajax({
            type: "GET",
            url: "/",
            success: function(res){
                $('#noti-box').text("0");
            }
       });
    });

    // 팀 즐겨찾기 ajax
    $(".subscribe-team").on("click", function(e){
        var card_link = $(this).parent().parent().parent().parent().attr('href');
        if(!card_link) {
            var link = window.location.pathname.split('/')[2];
        }
        else {
            var link = card_link.split('/')[2];
        }
        var icon = $(this).find('i')
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/subscribe/team/",
            data: {'pk': link },
            dataType:'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (res) {
                if(res.res == 1) icon.attr('class', 'fas fa-star');
                else icon.attr('class', 'far fa-star');
            },
            error: function (res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        });
    });
    // 팀 댓글 작성 ajax
    $('.post-comment-team').on("click", function(e){
        var path = '/comment/team/' + window.location.pathname.split('/')[3] +'/';
        var val = $(this).parent().find('textarea').val();
        $.ajax({
            type: "POST",
            url: path,
            data: {"content": val},
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (res) {
                location.reload();
            },
            error: function (res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        });
    });
    // 팀 댓글 삭제 ajax
    $('.delete-comment-team').on("click", function(e){
        var pk = $(this).data("id");
        $.ajax({
            type: "POST",
            url: "/comment/team/delete/",
            data: {'pk': pk},
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(res) {
                location.reload();
            },
            error: function(res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        })
    });
    // 대회 및 공모전 즐겨찾기 ajax
    $(".subscribe-contest").on("click", function(e){
        var card_link = $(this).parent().parent().parent().parent().attr('href');
        if(!card_link) {
            var link = window.location.pathname.split('/')[2];
        }
        else {
            var link = card_link.split('/')[2];
        }
        var icon = $(this).find('i')
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/subscribe/contest/",
            data: {'pk': link },
            dataType:'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (res) {
                if(res.res == 1) icon.attr('class', 'fas fa-star');
                else icon.attr('class', 'far fa-star');
            },
            error: function (res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        });
    });
    // 대회 및 공모전 댓글 작성 ajax
    $('.post-comment-contest').on("click", function(e){
        var path = '/comment/contest/' + window.location.pathname.split('/')[3] +'/';
        var val = $(this).parent().find('textarea').val();
        $.ajax({
            type: "POST",
            url: path,
            data: {"content": val},
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (res) {
                location.reload();
            },
            error: function (res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        });
    });
    // 대회 및 공모전 댓글 삭제 ajax
    $('.delete-comment-contest').on("click", function(e){
        var pk = $(this).data("id");
        $.ajax({
            type: "POST",
            url: "/comment/contest/delete/",
            data: {'pk': pk},
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(res) {
                location.reload();
            },
            error: function(res) {
              toastr.options = {
                  "closeButton" : true,
                  "positionClass": "toast-top-center",
                  timeOut: 10000,
              };
              toastr.warning(res.responseJSON.message);
            }
        })
    });
    // 회원 가입 ajax
    $('.signup-form').submit(function(e) {
        var button = $(this).find('button');
        $.ajax({
            type: "POST",
            url: "/signup/",
            data: $('.signup-form').serialize(),
            beforeSend: function() {
                button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                button.attr('disabled', true);
            },
            complete: function() {
                button.html('회원가입')
                button.attr('disabled', false);
            },
            success: function(res) {
                toastr.options = {
                  "positionClass": "toast-top-center",
                  timeOut: 3000,
                };
                var data = res.message;
                $.each(data, function(){
                    toastr.error($(this)[1]);
                });
                $("body").html(res.html).trigger("create");
            },
            error: function(res) {
                location.reload();
            },
        })
        e.preventDefault();
    });
    // 이메일 인증 (아이디 찾기) ajax
    $('.idfinder-form').submit(function(e) {
        var button = $(this).find('button');
        $.ajax({
            type: "POST",
            url: "/findid/",
            data: $('.idfinder-form').serialize(),
            beforeSend: function() {
                button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                button.attr('disabled', true);
            },
            complete: function() {
                button.html('인증메일 보내기')
                button.attr('disabled', false);
            },
            success: function(res) {
                toastr.options = {
                    "positionClass": "toast-top-center",
                    timeOut: 3000,
                };
                var data = res.message;
                $.each(data, function(){
                    toastr.error($(this)[1]);
                });
                $("body").html(res.html).trigger("create");
            },
            error: function(res) {
                toastr.options = {
                    "closeButton" : true,
                    "positionClass": "toast-top-center",
                    timeOut: 3000,
                };
                toastr.warning("등록된 사용자가 없습니다. 정보를 다시 확인해 주세요.");
            },
        })
        e.preventDefault();
    });
    // 이메일 인증 (비밀번호 찾기) ajax
    $('.pwfinder-form').submit(function(e) {
        var button = $(this).find('button');
        $.ajax({
            type: "POST",
            url: "/findpw/",
            data: $('.pwfinder-form').serialize(),
            beforeSend: function() {
                button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                button.attr('disabled', true);
            },
            complete: function() {
                button.html('인증메일 보내기')
                button.attr('disabled', false);
            },
            success: function(res) {
                toastr.options = {
                    "positionClass": "toast-top-center",
                    timeOut: 3000,
                };
                var data = res.message;
                $.each(data, function(){
                    toastr.error($(this)[1]);
                });
                $("body").html(res.html).trigger("create");
            },
            error: function(res) {
                toastr.options = {
                    "closeButton" : true,
                    "positionClass": "toast-top-center",
                    timeOut: 3000,
                };
                toastr.warning("등록된 사용자가 없습니다. 정보를 다시 확인해 주세요.");
            },
        })
        e.preventDefault();
    });
    // 글 작성 ajax
    $().submit(function() {
        $.ajax({
            type: "POST",
            url: "",
            success: function(res) {

            },
            error: function(res) {

            },
        })
    });
    // 자기소개 수정 ajax
    let self_intro = $('.self_intro_textarea').val()

    $('.self_intro_submit').on("click", (e) => {
        var path = '/member/detail/' + window.location.pathname.split('/')[3] +'/';
        self_intro = $('.self_intro_textarea').val();
        $.ajax({
            type: "POST",
            url: path,
            data: {"self_intro": self_intro},
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (res) {
                location.reload();
            },
            error: function (res) {
                alert("자기소개가 저장되지 않았습니다")
            }
        });
    });

});