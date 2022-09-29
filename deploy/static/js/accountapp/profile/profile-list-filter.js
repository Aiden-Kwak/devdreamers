$(document).ready(function(){
    $('#status-filter').SumoSelect({
        placeholder: '상태'
    });
    $('#type-filter').SumoSelect({
        placeholder: '지원 분야'
    });
    $('#type-filter').removeAttr('style');
    $('#status-filter').removeAttr('style');
    $('.CaptionCont').removeAttr('style');

    $('#interest-filter').tagator({
        filter: true,
        allowAutocompleteOnly: true,
        tag_container: '.interest-filter-tag'
    });
    $('#stack-filter').tagator({
        filter: true,
        allowAutocompleteOnly: true,
        tag_container: '.stack-filter-tag'
    });

    var interest_input = $('#interest-filter .tag-input');
    var stack_input = $('#stack-filter .tag-input');

    $('#interest-filter, #stack-filter').val('');
    $('.filter-tags').find('li').remove();
    $('.selected').removeClass('selected');

    $('#status-filter, #type-filter').on('change', function() {
        var a = $(this).siblings().children('.options').find('.selected');
        var id = $(this).attr('id');
        var container;
        if(id == 'status-filter') container = $('.status-filter-tag .tags-container')
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

    $('#initBtn').on('click', function() {
        $('#interest-filter, #stack-filter').val('');
        $('.filter-tags').find('li').remove();
        $('.selected').removeClass('selected');
        $('.filter-tags').trigger('change');
    });

    $('.filter-tags').on('change', function() {
        if($('.filter-tags').find('li').length == 0) $('#initBtn').hide();
        else $('#initBtn').show();
        var status = [], type = [];
        $('#status-filter').siblings().find('.selected').each(function() {
            status.push($(this).index());
        });
        $('#type-filter').siblings().find('.selected').each(function() {
            type.push($(this).index());
        });
        $.ajax({
            type: "GET",
            url: "/members/",
            data: {'interest':$('#interest-filter').val(),'stack':$('#stack-filter').val(),'status':status,'type':type},
            beforeSend: function() {
//                $('.wrap-loading').removeClass('d-none');
            },
            complete: function() {
//                $('.wrap-loading').addClass('d-none');
            },
            success: function(res) {
                $('.card-container').html(res.data);
                if(res.is_end) $('#loadMore').hide();
                else $('#loadMore').show();
            },
            error: function(request, status, error) {
                location.reload();
            },
        })
    });
    $('#loadMore').on("click", function() {
        var status = [], type = [];
        $('#status-filter').siblings().find('.selected').each(function() {
            status.push($(this).index());
        });
        $('#type-filter').siblings().find('.selected').each(function() {
            type.push($(this).index());
        });
        var offset = $(".profile-card").length;
        $.ajax({
            type: "GET",
            url: "/members/",
            data: {'interest':$('#interest-filter').val(),'stack':$('#stack-filter').val(),'status':status,'type':type,'offset': offset },
            dataType:'json',
            beforeSend:function() {
                $('#loadMore').attr('disabled', true);
                $('.wrap-loading').removeClass('d-none');
            },
            success: function (res) {
                $('.wrap-loading').addClass('d-none');
                $('#loadMore').attr('disabled', false);
                $('.card-container').append(res.data);
                if(res.is_end) {
                    $('#loadMore').hide();
                }
            },
            error: function (request, status, error) {
                location.reload();
            }
        });
    });
    $.ajax({
        type: "GET",
        url: "/autocomplete/interest/",
        beforeSend: function() {
            interest_input.next("ul").append('<li class="spinner autocomplete-option"><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span></li>')
        },
        complete: function() {
            interest_input.next("ul").find(".spinner").remove();
        },
        success: function(res) {
            var data = res.data;
            if(data) {
                data.sort(function (a, b) {
                    return a.toLowerCase().localeCompare(b.toLowerCase());
                });
                $('#interest-filter').tagator('autocomplete', data);
            }
        },
        error: function(request, status, error) {
            location.reload();
        },
    });

    $.ajax({
        type: "GET",
        url: "/autocomplete/stack/",
        beforeSend: function() {
            stack_input.next("ul").append('<li class="spinner autocomplete-option"><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span></li>')
        },
        complete: function() {
            stack_input.next("ul").find(".spinner").remove();
        },
        success: function(res) {
            var data = res.data;
            if(data) {
                data.sort(function (a, b) {
                    return a.toLowerCase().localeCompare(b.toLowerCase());
                });
                $('#stack-filter').tagator('autocomplete', data);
            }
        },
        error: function(request, status, error) {
            location.reload();
        },
    })

})