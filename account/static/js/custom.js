$(document).ready(function(){

	$(".navbar-toggler").click(function() {

		if ($( ".aside-menu" ).hasClass( "no-aside-menu" )){
			$(".aside-menu").removeClass("no-aside-menu");
			$(".wrapper .content-wrapper").css({"transform": "translate(320px,0)"});
			$(".canvas-overlay").css({"visibility": "visible","opacity": ".666"});	
			
		}
		else{
			$(".wrapper .content-wrapper").css({"transform": "translate(0,0)"});
			$(".aside-menu").addClass("no-aside-menu");
			$(".canvas-overlay").css({"visibility": "hidden"});
			$(".canvas-overlay").css({"opacity": "0"});

		}
	});


		$(".canvas-overlay").click(function() {
			$(".canvas-overlay").css({"visibility": "hidden"});
			$(".canvas-overlay").css({"opacity": "0"});
			$(".aside-menu").addClass("no-aside-menu");
			$(".wrapper .content-wrapper").css({"transform": "translate(0,0)"});
		});

});

