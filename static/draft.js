$(document).ready(function() {
    //$('#resultscontainer').load("/static/livetest.html");
    var refreshId = setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/draft",
            data:  "",
            success: function(html){
                $("#resultscontainer").load('/draft');
            }
        });
    }, 3000 );

});
