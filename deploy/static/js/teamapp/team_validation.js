function zeroPadded(val) {
  if (val >= 10)
    return val;
  else
    return '0' + val;
}
$(document).ready(function() {

    d = new Date();
    $('input[type=datetime-local]').attr('min',d.getFullYear()+"-"+zeroPadded(d.getMonth() + 1)+"-"+zeroPadded(d.getDate())+"T"+zeroPadded(d.getHours())+":"+ zeroPadded(d.getMinutes()));

    $("input[name=title]").on("change input", function(e) {
        if($(this).val().length > 31) {
            toastr.options = {
                "closeButton" : true,
                "positionClass": "toast-top-center",
                "timeOut": 3000,
            }
            toastr.warning("글자 입력제한을 초과했습니다.");
            $(this).val('');
        }
    });

    $("input[name=description]").on("change input", function(e) {
        if($(this).val().length > 46) {
            toastr.options = {
                "closeButton" : true,
                "positionClass": "toast-top-center",
                "timeOut": 3000,
            }
            toastr.warning("글자 입력제한을 초과했습니다.");
            $(this).val('');
        }
    });

    $("input[name=contact]").on("change input", function(e) {
        if($(this).val().length > 257) {
            toastr.options = {
                "closeButton" : true,
                "positionClass": "toast-top-center",
                "timeOut": 3000,
            }
            toastr.warning("글자 입력제한을 초과했습니다.");
            $(this).val('');
        }
    });

    $("input[name='category']").on("click", function(e){
        var cnt = $("input[name='category']:checked").length;
        if(cnt>3){
            toastr.options = {
                "closeButton" : true,
                "positionClass": "toast-top-center",
                "timeOut": 3000,
            }
            toastr.warning("최대 3개까지 선택 가능합니다!");
            e.preventDefault();
        }
    });

    $('form').on('submit', function(e){
        var cnt = $("input[name='category']:checked").length;
        if(cnt == 0) {
            toastr.options = {
                "closeButton" : true,
                "positionClass": "toast-top-center",
                "timeOut": 3000,
            }
            toastr.warning("모집 분야를 선택해주세요!");
            e.preventDefault();
        }
    });
});