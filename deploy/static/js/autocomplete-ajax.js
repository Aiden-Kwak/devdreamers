$(document).ready(function(){
    $('#interest-search-field').tagator({});
    $('#stack-search-field').tagator({});

    var interest_input = $('#interest-search-field .tag-input');
    var stack_input = $('#stack-search-field .tag-input');

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
                $('#interest-search-field').tagator('autocomplete', data);
            }
        },
        error: function(res) {
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
                $('#stack-search-field').tagator('autocomplete', data);
            }
        },
        error: function(res) {
            location.reload();
        },
    })
});