//update the info
$(function() {
	$('#Update').click(function() {
		updateinfo();
	});

	var Nickname = $('#Nickname').attr('value');
	var Email = $('#Email').attr('value')
	
	function updateinfo() {
		var post = [nickname=Nickname,email=Email];
		var url = "/update";
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

