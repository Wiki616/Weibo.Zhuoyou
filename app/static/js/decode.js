$(document).ready(function(e){
	$(".weibocontent").each(function(e){
		var href = $(this).children(":nth(0)");
		var txt = href.html();
		href.html("");
		href.html(txt.replace(/&lt;/g, '<').replace(/&gt;/g, '>'));
	});
});