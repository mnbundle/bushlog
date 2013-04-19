initLikeButton = function () {
    var csrftoken = $.cookie('csrftoken');

    var btn = $('.like');
    var count_ele = $('.like-count');
    var icon_ele = $('.like-icon');
    var text_ele = $('.like-text');

    if (btn.data('count')) {
        var current_count = parseInt(btn.data('count'));
    }
    else {
        current_count = 0;
    }
    count_ele.text(current_count);

    btn.click(function () {
        if (!$(this).hasClass('disabled')) {
            $.post(
                '/action/like/' + $(this).data('type') + '/',
                {id: $(this).data('oid'), csrfmiddlewaretoken: csrftoken},
                function (data) {
                    if (data.success) {
                        text_ele.text("Liked");
                        icon_ele.removeClass('icon-star-empty').addClass('icon-star');
                        count_ele.text(current_count + 1);
                        btn.addClass('disabled').unbind('click');
                    }
                }
            );
        }
    });
}
