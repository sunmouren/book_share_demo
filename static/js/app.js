
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

    tips(comment_text, 'danger');

    if (comment_text == '') {
        tips('评论不能为空！', 'danger');
        return false;
    }
    // $.ajax({
    //     cache: false,
    //     type: "POST",
    //     data: {'aid': aid, 'pid': parseInt(pid), 'content': comment_text},
    //     url: "/comment/submit/",
    //     async: true,
    //     beforeSend : function () {
    //         pageLoader('show'); // loading
    //     },
    //     //成功返回之后调用的函数
    //     success:function(data){
    //         if (data['msg'] == 'ok') {
    //             tips('评论提交成功，页面即将刷新~', 'success');
    //             $("#commentarea_"+pid).val("");
    //             setTimeout(function () {
    //                 location.reload();
    //                 window.location.href= location.href + '#recentcomments';
    //             }, 1500);
    //             return true;
    //         } else {
    //             tips('评论出错啦！Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
    //             return false;
    //         }
    //     },
    //     complete: function () {
    //         pageLoader('hide');
    //     },
    //
    //     //调用出错执行的函数
    //     error: function(){
    //         tips('好气啊 提交失败啦 Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
    //         return false;
    //     }
    // });
}

// 取消评论
function cancelComment(id) {
	$('#CommentForm' + id).collapse('hide');
}