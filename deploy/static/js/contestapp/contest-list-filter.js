$(document).ready(function(){
    $('#category-filter').SumoSelect({
        placeholder: '분야'
    });
    $('#category-filter').removeAttr('style');
    $('.CaptionCont').removeAttr('style');

    $('.filter-tags').find('li').remove();
    $('.selected').removeClass('selected');

    $('#category-filter').on('change', function() {
        var a = $(this).siblings().children('.options').find('.selected');
        var id = $(this).attr('id');
        var container;
        if(id == 'category-filter') container = $('.category-filter-tag .tags-container')
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

    $("#title-filter, #host-filter").on('input', function() {
        $('.filter-tags').trigger('change');
    });

    $(".align-change").change(function() {
        $('.filter-tags').trigger('change');
    });

    $('#initBtn').on('click', function() {
        $('#title-filter, #host-filter').val('');
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
        $.ajax({
            type: "GET",
            url: "/contest/",
            data: {'title':$('#title-filter').val(),'host':$('#host-filter').val(),'category':category,'type':type,'checked':$('.align-change')[0].checked ? 1 : 0},
            beforeSend: function() {
//                $('.wrap-loading').removeClass('d-none');
            },
            complete: function() {
//                $('.wrap-loading').addClass('d-none');
            },
            success: function(res) {
                $('.card-container-contest').html(res.data)
                if(res.is_end) $('#loadMore').hide();
                else $('#loadMore').show();
                view_fc()
                deadline_fc()
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
        var offset = $(".contest-card").length;
        $.ajax({
            type: "GET",
            url: "/contest/",
            data: {'title':$('#title-filter').val(),'host':$('#host-filter').val(),'category':category,'type':type, 'offset':offset, 'checked':$('.align-change')[0].checked ? 1 : 0},
            dataType:'json',
            beforeSend:function() {
                $('#loadMore').attr('disabled', true);
                $('.wrap-loading').removeClass('d-none');
            },
            success: function (res) {
                $('.wrap-loading').addClass('d-none');
                $('#loadMore').attr('disabled', false);
                $('.card-container-contest').append(res.data);
                if(res.is_end) {
                    $('#loadMore').hide();
                }
                view_fc()
                deadline_fc()
            },
            error: function (request, status, error) {
                location.reload();
            }
        });
    });
})