$(document).ready(function() {
    $('.nice-select').niceSelect();
    $('.upload-image').on("click", function() {
        $('.input-image').click();
    })

    $('.profile-del-image').on("click", function() {
        $('.input-image').val('');
        $('.preview-image').css("background-image","url(/static/img/profile-default.png)");
    })
    $('.team-del-image').on("click", function() {
        $('.input-image').val('');
        $('.preview-image').css("background-image","url(/static/img/team-default.jpg)")
    })
    $('.input-image').on("change", function() {

        var files = $('.input-image')[0].files;
        var reader = new FileReader();

        reader.readAsDataURL(files[0]);

        reader.onload = function(e) {
            $('.preview-image').css("background-image","url("+ reader.result +")");
        };
    })
});