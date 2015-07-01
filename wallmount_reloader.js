var wallmount_reloader = function () {
    var SOURCE_URL = "http://192.168.1.39:8000/sketch";
    var last_push_id = "no_id";
    setInterval(maybe_reload, 5000);

    function maybe_reload() {
        if (need_to_reload()) {
            var iframe = document.getElementById("sketch_iframe");
            iframe.src = SOURCE_URL;
        }
    }

    function need_to_reload() {
        // TODO: Request push_id from the server.
        
    }
}

wallmount_reloader();
