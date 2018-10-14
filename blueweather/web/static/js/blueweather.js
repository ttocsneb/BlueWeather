
// Show the sidebar if the screen is larger than 'sm'
if($(window).width() >= 768) {
    $(".sidebar").removeClass("toggled");
    $("#page-top").removeClass("sidebar-toggled");
    console.log('minified the menu');
}

is_down = false;

$(document).ready(function() {
    setInterval(function() {
        $.get("/isDown", function() {
            if(is_down) {
                console.log('Server Back Up!, Reloading!');
                location.reload();
            }
        }).fail(function() {
            $("#site_down").modal("show");
            is_down = true;
        });
    }, 15000);
});