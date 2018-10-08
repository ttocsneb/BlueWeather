function weather_render(data) {
    $('#weather-content').html(data);
}

function weather_update() {
    $.get('/data/weather', function(data) {
        weather_render(data);
    });
}

window.addEventListener("load", function(event) {
    setInterval(weather_update, 15*1000);
});