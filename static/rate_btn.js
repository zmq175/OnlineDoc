$(document).ready(function () {
   $.getJSON("/check_rate_status/?id=" + id,function (json) {
    if(json.rate === 1){
        $("#like").attr("disabled", "disabled");
        $("#dislike").attr("disabled", "disabled");
    }
});
   $.getJSON("/check_favorite_status/?id=" + id,function (json) {
       if (json.favorite === 1){
           $("#favorite").attr("disabled", "disabled");
       }
   });
});
$("#favorite").click(function () {
    $.get("/add_to_favorite/?id=" + id, function (data, status) {
        $("#favorite").attr("disabled", "disabled");
    })
});
$("#like").click(function () {
    $.get("/likes_change/?id=" + id + "&direct=1", function (data, status) {
        var likes = $("#like").text();
        likes = parseInt(likes) + 1;
        $("#like").html("<i class=\"fa fa-thumbs-up\"></i> " + likes);
        $("#like").attr("disabled", "disabled");
        $("#dislike").attr("disabled", "disabled");
    })
});
$("#dislike").click(function () {
    $.get("/dislikes_change/?id=" + id + "&direct=1", function (data, status) {
        var dislikes = $("#dislike").text();
        dislikes = parseInt(dislikes) + 1;
        $("#dislike").html("<i class=\"fa fa-thumbs-down\"></i> " + dislikes);
        $("#like").attr("disabled", "disabled");
        $("#dislike").attr("disabled", "disabled");
    })
});