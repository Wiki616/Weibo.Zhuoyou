//update the info
$(function() {
	$('#Share').click(function() {
		updateweibo();
	});
	
	function updateweibo() {
		var username = $('#Nick').html();
		var content = $('#weibo').val();
		var d = new Date()
		var year = d.getFullYear()
		var mon = d.getMonth() + 1
		var day = d.getDate()
		var h = d.getHours();
		var m = d.getMinutes();
		var s = d.getSeconds();
		
		var pre = $('#bigtable').html();
		var newpart = '<div class = "row"> <div class="col-md-7"> <div class="thumbnail"> <div class = "row"> <div class="col-md-1">' +
			'<img src="/static/pic/icon.jpg" height="48" width="48" href=""></img>' +
			'</div> <div class="col-md-11"> <div class="row"> <div class="col-md-6">' +
			'<a class="text-left" href=""><h4><b>' + username + '</b></h4></a>' +
			'</div> <div class="col-md-3 col-md-offset-3"> <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button> </div> </div> ' +
			'<div class="row"> <div class="col-md-12">' +
			'<label ><h4>' + content + '</h4></label>' +
			'</div> </div> </div>' +
			'<div class="col-md-3">' + 
			'<p class="text-center"><h5><small>' + year + '-' + mon + '-' + day + ' ' + h + ':' + m + '</small></h5></p>' +
			'</div> <div class="col-md-2 col-md-offset-3"> <a class="text-left" href=""><h5><b><span class="glyphicon glyphicon-new-window"></span> Forward!</b></h5></a> </div> <div class="col-md-2"> <a class="text-left" href=""><h5><b><span class="glyphicon glyphicon-pencil"></span> Commit!</b></h5></a> </div> <div class="col-md-2"> <a class="text-left" href=""><h5><b><span class="glyphicon glyphicon-thumbs-up"></span> Like!</b></h5></a> </div> </div> </div> </div> </div>';
		$('#bigtable').html(newpart + pre);
	}
});