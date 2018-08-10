
function status_render(data) {
    $('#status-content').html(data)
}

function status_update() {
    $.get('/data/status', function(data) {
        status_render(data);
    });
}

function status_remove(key) {
    $.get(`/status/remove_message?id=${key}`, function(data) {
        if(data != 'false') {
            status_render(data);
        }
    });
}

window.addEventListener("load", function(event) {
    setInterval(status_update, 15*1000);
});