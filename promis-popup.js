	function showPromisPopup() {
        var key = '9fb2c4425b39e09d26f18c2e8a2ff0d796576106d3794c9aa8ad73e3b0588b785bdf1f5b6c2f8cd0653ecbcda48ed11ad85dce9c9680777458c965e285fff17b';
        var rsa = new RSAKey();
        rsa.setPublic(key, '10001');
        
	var str = $( ".printheader" ).text();
	var mrn = str.substr(str.indexOf("MRN: ") + 5, 8);
	var encryptedMrn = rsa.encrypt(mrn);

	var qIdStr = $( "#q1" ).attr("data-lql");
	qIdStr = qIdStr.substring(qIdStr.indexOf('LQF_') + 4,qIdStr.indexOf('_LQL_'));
	var encryptedQId = rsa.encrypt(qIdStr);

	//var url = "https://promis.webstg.nyumc.org/proms/current/web/app_stg.php";
    var url = "https://promis.nyulmc.org/proms/current/web";
	//var url = "https://promis.webdev.nyumc.org/proms/current/web/app_dev.php";
	
	url += "/mychartstart?mrn="+encryptedMrn+"&qid="+encryptedQId;

	var $close = $("<a/>").addClass("close-btn");
	var $div = $("<div/>").addClass("promis-popup");
	if($(window).width()<768) $div.addClass("is-mobile");

	var $iframe = $("<iframe/>").attr("src", url);
	$close.appendTo($div);
	$iframe.appendTo($div);
	$div.appendTo("body").fadeIn();	
	var $overlay = $("<div></div>").addClass("promis-popup-overlay");
	$overlay.appendTo("body");

	$close.click(function(e) {	
		e.preventDefault();
		$div.remove();
		$overlay.remove();
	});	
}
$(function() {
	var $link = $('<a href="#" class="promis-link"> <b><u>Click here</u></b> </a><span> <b> to open your assessment</b></span>'), 
		$promisDiv = $('.promisdiv');

	$link.click(function(e) {	
		e.preventDefault();
		showPromisPopup();
	});
	
	$promisDiv.append($link);
});