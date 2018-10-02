
var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type == 'success' ? 'animated fadeInUp' : 'animated shake';

	jQuery.notify({
		icon: $icon,
		message: $msg
	},
	{
		element: 'body',
		type: $type,
		allow_dismiss: true,
		newest_on_top: true,
		showProgressbar: false,
		placement: {
			from: $from,
			align: $align
		},
		offset: 20,
		spacing: 10,
		z_index: 10800,
		delay: 3000,
		timer: 1000,
		animate: {
			enter: $enter,
			exit: 'animated fadeOutDown'
		}
	});
};


/*  发表书评 */
function submitComment(bid, pid){
     // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#message-text-" + bid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var comment_text = $.trim($("#message-text-" + bid).val());

    if (comment_text == '') {
        tips('评论不能为空！', 'danger');
        return false;
    }
    $.ajax({
        cache: false,
        type: "POST",
        data: {'bid': bid, 'pid': parseInt(pid), 'content': comment_text},
        url: "/comment/submit/",
        async: true,
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('评论提交成功，页面即将刷新~', 'success');
                $("#message-text-" + bid).val("");
                setTimeout(function () {
                    location.reload();
                    window.location.href= location.href + '#recent';
                }, 1500);
                return true;
            } else {
                tips('评论出错啦！Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
                return false;
            }
        },
        //调用出错执行的函数
        error: function(){
            tips('好气啊 提交失败啦 Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
            return false;
        }
    });
}

/* 回复 */
function submitReply(bid, pid){
     // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#message-text-" + pid).data('login');
    if(login == 'unlogin'){
        tips('请登入后操作！', 'danger');
        window.location.href = '/user/login/';
        return false;
    }
    var comment_text = $.trim($("#message-text-" + pid).val());

    if (comment_text == '') {
        tips('评论不能为空！', 'danger');
        return false;
    }
    $.ajax({
        cache: false,
        type: "POST",
        data: {'bid': bid, 'pid': parseInt(pid), 'content': comment_text},
        url: "/comment/submit/",
        async: true,
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('回复书评成功，页面即将刷新~', 'success');
                $("#message-text-" + pid).val("");
                setTimeout(function () {
                    location.reload();
                    window.location.href= location.href + '#recent';
                }, 1500);
                return true;
            } else {
                tips('评论出错啦！Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
                return false;
            }
        },
        //调用出错执行的函数
        error: function(){
            tips('好气啊 提交失败啦 Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
            return false;
        }
    });
}

// 取消书评表单
function cancelComment(id) {
	$('#CommentForm' + id).collapse('hide');
}

// 删除评论
function deleteComment(bid) {
    $.ajax({
        cache: false,
        type : "POST",
        data : {'bid': parseInt(bid)},
        url : "/comment/delete/",
        async: true,
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('删除成功~', 'success');
                setTimeout(function () {
                    $('#comment-'+bid).remove();
                }, 1000);

            }else {
                tips('好气~ 删除失败!', 'danger');
            }
        },
        //调用出错执行的函数
        error: function(){
            tips('好气~ 提交失败!', 'danger');
        }
    });
}

/* 喜欢评论 */
function SubmitLike(bid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#like-comment-"+bid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#like-comment-"+bid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/comment/like/",
        data: {'bid': bid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#like-comment-"+bid).data('action', action == 'like' ? 'unlike' : 'like');
                var previous_likes = parseInt($("#like-count-"+bid).text());
                if ($("#like-comment-"+bid).hasClass("text-info")) {
                    $("#like-comment-"+bid).removeClass("text-info");
                    $("#like-comment-"+bid).addClass("text-danger");

                    $("#like-count-"+bid).text(previous_likes + 1);
                    tips('+1', 'success');
                } else {
                    $("#like-comment-"+bid).removeClass("text-danger");
                    $("#like-comment-"+bid).addClass("text-info");

                    $("#like-count-"+bid).text(previous_likes - 1)
                    tips('-1', 'success');
                }
            }
        },
    });
}

/* 关注用户 */
function FollowUser(uid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#follow-user-"+uid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#follow-user-"+uid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/user/follow/",
        data: {'uid': uid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#follow-user-"+uid).data('action', action == 'follow' ? 'unfollow' : 'follow');
                if ($("#follow-user-"+uid).hasClass("text-success")) {
                    $("#follow-user-"+uid).removeClass("text-success");
                    $("#follow-user-"+uid).html('<i class="fa fa-plus"></i> 关注');
                } else {
                    $("#follow-user-"+uid).addClass("text-success");
                    $("#follow-user-"+uid).html('<i class="fa fa-check"></i> 已关注');
                }
            }
        },
    });
}

