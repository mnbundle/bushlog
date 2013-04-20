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
            $.post('/action/like/' + $(this).data('type') + '/', {
                id: $(this).data('oid'),
                csrfmiddlewaretoken: csrftoken
            }, function (data) {
                if (data.success) {
                    text_ele.text("Liked");
                    icon_ele.removeClass('icon-star-empty').addClass('icon-star');
                    count_ele.text(current_count + 1);
                    btn.addClass('disabled').unbind('click');
                }
            });
        }
    });
}

removePost = function () {
    var csrftoken = $.cookie('csrftoken');
    var type = $(this).data('type');
    var comment_id = $(this).data('comment_id');
    var self = $(this);

    $.ajax({
        url: '/action/comment/' + type + '/' + comment_id + '/',
        type: 'DELETE',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            if (data.success) {
                self.parent().slideUp("slow");
            }
        }
    });
}

initCommentForm = function () {
    var csrftoken = $.cookie('csrftoken');

    var btn = $('.btn-comment');
    var btn_close = $('.close-comment');
    var count_ele = $('.comment-count');
    var comment_ele = $('.comment:visible');
    var comment_container = $('.container-comment');

    comment_ele.autogrow();

    if (btn.data('count')) {
        var current_count = parseInt(btn.data('count'));
    }
    else {
        current_count = 0;
    }

    count_ele.text(current_count);
    btn_close.click(removePost).click( function () {
        count_ele.text(current_count - 1);
    });

    btn.click(function () {
        if (!$(this).hasClass('disabled')) {
            var oid = $(this).data('oid');
            var comment = comment_ele.val();
            var type = $(this).data('type');

            if (!comment) {
                return false;
            }

            comment_ele.attr('readonly', true).addClass('wait');

            $.post('/action/comment/' + type + '/', {
                csrfmiddlewaretoken: csrftoken,
                id: oid,
                comment: comment
            }, function (data) {
                if (data.success) {
                    btn.addClass('disabled').unbind('click');
                    var avatar = "/static/img/layout/profile-" + data.object.user.gender + ".png";
                    if (data.object.user.avatar) {
                        avatar = data.object.user.avatar;
                    }

                    var comment_item = $('<div class="media"> \
                        <button type="button" class="close close-comment pull-right" data-comment_id="' + data.object.id + '" data-type="' + type + '">&times;</button> \
                        <img class="media-object img-rounded pull-left" src="' + avatar + '" width="35" height="35" onclick="window.location=\'' + data.object.user.url + '\'"/> \
                        <div class="media-body"> \
                            <blockquote class="comment">' + data.object.comment + '<small>' + data.object.fuzzy_date_added + '</small></blockquote> \
                        </div> \
                    </div>').hide().prependTo(comment_container).slideDown("slow");

                    comment_ele.val('').removeAttr('readonly').removeClass('wait');
                    comment_item.children('.close-comment').click(removePost).click( function () {
                        count_ele.text(current_count - 1);
                    });

                    count_ele.text(current_count + 1);
                }
            });
        }
        return false;
    });
}
