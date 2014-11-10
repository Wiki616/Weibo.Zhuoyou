//update the info
$(function() {
	$('#Update').click(function() {
		updateinfo();
	});

	var Username = $.cookie('username')
	var Nickname = $('#Nickname').attr('value');
	var Email = $('#Email').attr('value')
	
	function updateinfo() {
		var post = [uesrname = Username,nickname=Nickname,email=Email];
		var url = "/update1";
		//location.href = url;
		$.ajax({
            type : "POST",
            url : url,
			data : post,
            success: function(msg) {
                        alert("Ok!")
					}
		});
	}
});

