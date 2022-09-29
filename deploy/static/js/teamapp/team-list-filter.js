$(document).ready(function(){
    $('#category-filter').SumoSelect({
        placeholder: '모집분야'
    });
    $('#type-filter').SumoSelect({
        placeholder: '팀 종류'
    });
    $('#type-filter').removeAttr('style');
    $('#category-filter').removeAttr('style');
    $('.CaptionCont').removeAttr('style');

    $('.filter-tags').find('li').remove();
    $('.selected').removeClass('selected');

    $('#category-filter, #type-filter').on('change', function() {
        var a = $(this).siblings().children('.options').find('.selected');
        var id = $(this).attr('id');
        var container;
        if(id == 'category-filter') container = $('.category-filter-tag .tags-container')
        else container = $('.type-filter-tag .tags-container')
        container.html('');
        a.each(function(){
            var t = $(this).text();
            var li = $(document.createElement('li')).addClass('tag-item').text(t);
            var a = $(document.createElement('a')).addClass('select-item-remove').text('X');
            a.on('click', function(){
                $('select#'+id)[0].sumo.unSelectItem(t);
            });
            li.append(a);
            container.append(li);
        });
        $('.filter-tags').trigger('change');
    });

    $("#title-filter, #nickname-filter").on('input', function() {
        $('.filter-tags').trigger('change');
    });

    $('#initBtn').on('click', function() {
        $('#title-filter, #nickname-filter').val('');
        $('.filter-tags').find('li').remove();
        $('.selected').removeClass('selected');
        $('.filter-tags').trigger('change');
    });

    $('.filter-tags').on('change', function() {
        if($('.filter-tags').find('li').length == 0) $('#initBtn').hide();
        else $('#initBtn').show();
        var category = [], type = [];
        $('#category-filter').siblings().find('.selected').each(function() {
            category.push($(this).text());
        });
        $('#type-filter').siblings().find('.selected').each(function() {
            type.push($(this).index());
        });
        $.ajax({
            type: "GET",
            url: "/teams/",
            data: {'title':$('#title-filter').val(),'nickname':$('#nickname-filter').val(),'category':category,'type':type},
            beforeSend: function() {
//                $('.wrap-loading').removeClass('d-none');
            },
            complete: function() {
//                $('.wrap-loading').addClass('d-none');
            },
            success: function(res) {
                $('.card-container-team').html(res.data);
                if(res.is_end) $('#loadMore').hide();
                else $('#loadMore').show();
            },
            error: function(request, status, error) {
                location.reload();
            },
        })
    });
    $('#loadMore').on("click", function() {
        var category = [], type = [];
        $('#category-filter').siblings().find('.selected').each(function() {
            category.push($(this).text());
        });
        $('#type-filter').siblings().find('.selected').each(function() {
            type.push($(this).index());
        });
        var offset = $(".team-card").length;
        $.ajax({
            type: "GET",
            url: "/teams/",
            data: {'title':$('#title-filter').val(),'nickname':$('#nickname-filter').val(),'category':category,'type':type, 'offset':offset},
            dataType:'json',
            beforeSend:function() {
                $('#loadMore').attr('disabled', true);
                $('.wrap-loading').removeClass('d-none');
            },
            success: function (res) {
                $('.wrap-loading').addClass('d-none');
                $('#loadMore').attr('disabled', false);
                $('.card-container-team').append(res.data);
                if(res.is_end) {
                    $('#loadMore').hide();
                }
            },
            error: function (request, status, error) {
                location.reload();
            }
        });
    });
})