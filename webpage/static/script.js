$(document).ready(function(){

	function hit_endpoint(endpoint){
		//alert("hitting endpoint " + endpoint);
		$("#text_area").text(endpoint);
		url = "http://192.168.1.1/" + endpoint;
	    $.ajax({url: url, 
	        type:"GET",                    
	        success: function(data) { alert("succsess") }
	    });
	}

	$("#stop").click(function(){
	    hit_endpoint("manual/stop");
	});

	$("#mode_manual").click(function(){
	    hit_endpoint("mode/manual");
	});

	$("#mode_auto").click(function(){
	    hit_endpoint("mode/auto");
	});

	// Directions Mouse Down
	$("#up").mousedown(function(){
	    hit_endpoint("manual/forward");
	});

	$("#down").mousedown(function(){
	    hit_endpoint("manual/backward");
	});

	$("#left").mousedown(function(){
	    hit_endpoint("manual/left");
	});

	$("#right").mousedown(function(){
	    hit_endpoint("manual/right");
	});

	// Directions Mouse Up
	$("#up").mouseup(function(){
	    hit_endpoint("manual/stop");
	});

	$("#down").mouseup(function(){
	    hit_endpoint("manual/stop");
	});

	$("#left").mouseup(function(){
	    hit_endpoint("manual/stop");
	});

	$("#right").mouseup(function(){
	    hit_endpoint("manual/stop");
	});

	// Direction Arrow Keys Down
	$('html').keydown(function(e){
       switch(e.which) {
        case 37: // left
        	$("#left").addClass('active');
        	$("#left").mousedown();
        break;

        case 39: // right
        	$("#right").addClass('active');
        	$("#right").mousedown();
        break;

        case 38: // up
        	$("#up").addClass('active');
        	$("#up").mousedown();
        break;

        case 40: // down
        	$("#down").addClass('active');
        	$("#down").mousedown();
        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
    });

	// Direction Arrow Keys up
	$('html').keyup(function(e){
       switch(e.which) {
        case 37: // left
        	$("#left").removeClass('active');        	
        	$("#left").mouseup();
        break;

        case 39: // right
        	$("#right").removeClass('active');       	
        	$("#right").mouseup();
        break;

        case 38: // up
        	$("#up").removeClass('active');
        	$("#up").mouseup();
        break;

        case 40: // down
        	$("#down").removeClass('active');
        	$("#down").mouseup();
        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
    });


});