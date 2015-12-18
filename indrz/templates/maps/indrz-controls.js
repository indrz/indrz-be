var full_screen_control = new ol.control.FullScreen({
    label: "Go Full Screen",
    className: "btn-fullscreen",
    target: document.getElementById("id-fullscreen")
});


map.addControl(full_screen_control);