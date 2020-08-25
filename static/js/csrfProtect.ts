/// <reference types="jquery" />
/// <reference types="lodash" />

const csrftoken = Cookies.get('csrftoken')

$.ajaxSetup({
    beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }
})