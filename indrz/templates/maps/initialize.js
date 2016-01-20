$(document).ready(function(){
    function initialize() {
        if (floor_layers.length > 0) {
            if(route_from!='' && route_to !=''){
                $("#route-from").val(route_from);
                $("#route-to").val(route_to);
            }
            $("#submitForm").submit();
        } else {
            setTimeout(initialize, 250);
        }
    }
    initialize();
});