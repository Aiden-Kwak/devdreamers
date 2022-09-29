$(document).ready(function() {

    $(document).on("click", ".add-form", function() {
        var form = $(this).parent().eq(0).clone();
        form.find("input, textarea, select").each(function() {
            var name = $(this).attr('name');
            name_arr = name.split('_');
            name = name_arr[0] + '_' + (parseInt(name_arr[1]) + 1);
            $(this).attr('name', name);
        });
        form.find("input[type=text], textarea").val("");
        form.find(".current").text(form.find("select option").first().text());
        form.find(".list .selected").attr("class", "option");
        $(this).text("-")
        $(this).attr("class", "del-form")
        $(this).parent().parent().append(form)
    });

    $('.numeric-form').on('change input', function(e) {
        var isMonth = $(this).attr('maxLength') == 2 ? true : false;
        if($(this).val().replace(/\d+/g, "").length) {
            toastr.options = {
                closeButton: !0,
                positionClass: "toast-top-center",
                timeOut: 1e3
            };
            toastr.warning("날짜 형식에 맞게 입력해주세요!");
            $(this).val("");
            return false
        }
        var val = Number($(this).val());
        if(isMonth && (val < 1 || val > 12)) {
            toastr.options = {
                closeButton: !0,
                positionClass: "toast-top-center",
                timeOut: 1e3
            };
            toastr.warning("날짜 형식에 맞게 입력해주세요!");
            $(this).val("");
            return false;
        }
    });

    $(document).on("click", ".del-form", function () {
        $(this).parent().remove();
        var class_name = $(this).siblings("div:first").attr("class").split(" ")[1];
        var i = 0;
        $("." + class_name).each(function() {
//            console.log($(this));
            $(this).find("input, textarea, select").each(function() {
                var name = $(this).attr('name');
                name_arr = name.split('_');
                name = name_arr[0] + '_' + i;
                $(this).attr('name', name);
            });
            i += 1;
        });
    });

    $("form").submit(function (t) {
        var activity_num = $('.activity-form').length;
        var lang_num = $('.lang-form').length;
        var cert_num = $('.cert-form').length;
        var award_num = $('.award-form').length;
        var intern_num = $('.intern-form').length;

		$(this).append('<input type="hidden" name="activity_num"/>');
		$("input[name='activity_num']").val(activity_num);

		$(this).append('<input type="hidden" name="lang_num"/>');
		$("input[name='lang_num']").val(lang_num);

		$(this).append('<input type="hidden" name="cert_num"/>');
		$("input[name='cert_num']").val(cert_num);

		$(this).append('<input type="hidden" name="award_num"/>');
		$("input[name='award_num']").val(award_num);

		$(this).append('<input type="hidden" name="intern_num"/>');
		$("input[name='intern_num']").val(intern_num);
	})
});