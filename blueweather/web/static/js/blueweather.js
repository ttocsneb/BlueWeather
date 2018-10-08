
// Show the sidebar if the screen is larger than 'sm'
if($(window).width() >= 768) {
    $(".sidebar").removeClass("toggled");
    $("#page-top").removeClass("sidebar-toggled");
    console.log('minified the menu');
}