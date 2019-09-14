var switchableLayers = [wmsE00, wmsE01, wmsE02, wmsE03];

function getActiveFloorNum(){

 return active_floor_num

}


function waitForFloors(space_floor_id) {
    if (floor_layers.length > 0) {

        // for (var i = 0; i < floors_info.length; ++i) {
        //     floor_layers.push(floors_info[i]);
        //     appendFloorNav(floors_info[i].short_name, [i]);
        //     }

        activateLayer(space_floor_id);


        // for (var i = 0; i < building_info.num_floors; i++) {
        //     if (building_info.buildingfloor_set[i].id == space_floor_id) {
        //         activateLayer(i);
        //     }
        // }
    }
    else {
        setTimeout(function () {
            waitForFloors(space_floor_id);
        }, 250);
    }
}


function hideLayers() {
    for (var i = 0; i < switchableLayers.length; i++) {
        switchableLayers[i].setVisible(false);
    }
    // if (floor_layers.length > 0) {
    //     for (var i = 0; i < floor_layers.length; i++) {
    //         floor_layers[i].setVisible(false);
    //     }
    // }
    $("#floor-links li").removeClass("active");
}



function setRouteStyle(layer){
    var features = layer.getSource().getFeatures();
    for (var i = 0; i < features.length; i++) {
        var feature_floor = features[i].getProperties().floor;
        if (feature_floor == active_floor_num) {
            features[i].setStyle(route_active_style);
        } else {
            features[i].setStyle(route_inactive_style);
        }
    }

}

function setLayerVisible(index) {

    // switchableLayers[index].setVisible(true);
    if (switchableLayers.length > 0) {
        switchableLayers[index].setVisible(true);
        $("#floor-links li:nth-child(" + (switchableLayers.length - index) + ")").addClass("active");

        // set active_floor_num
        active_floor_num = switchableLayers[index].getProperties().floor_num;
        if (routeLayer || libraryRouteLayer) {

            if(routeLayer){
                setRouteStyle(routeLayer);
            }else {
                setRouteStyle(libraryRouteLayer);
            }

        }
        if (searchLayer) {

            var len_searchRes = searchLayer.getProperties().source.getFeatures().length;
            if (len_searchRes < 2 && len_searchRes !== 0 ){
                // console.log("length search res " + len_searchRes)
                var floor_searchLayer = searchLayer.getProperties().source.getFeatures()[0].getProperties().floor_num;
                if(floor_searchLayer === active_floor_num){
                    searchLayer.setVisible(true);
                }else{
                    searchLayer.setVisible(false);
                }

            }else{
                var sfeatures = searchLayer.getSource().getFeatures();
                for (var s = 0; s < sfeatures.length; s++) {
                    var sfeature_floor = sfeatures[s].getProperties().floor_num;
                    // console.log("we are in set visible layer "+ typeof active_floor_num);
                    //
                    // console.log(searchLayer.getProperties().source.getFeatures()[0].getGeometry().getType());


                    if (typeof sfeature_floor === "number"){
                        sfeature_floor = sfeature_floor.toString();

                    }


                    var geoType = sfeatures[s].getGeometry().getType();

                    // console.log(sfeature_floor);
                    if (sfeature_floor === active_floor_num) {


                        if (geoType === "MultiPoint"){
                            sfeatures[s].setStyle(styleFunction);

                        }else{
                            sfeatures[s].setStyle(show_search_style);

                        }


                    } else {


                        if (geoType === "MultiPoint"){
                            sfeatures[s].setStyle(styleFunctionHide);

                        }else{
                            sfeatures[s].setStyle(hide_search_style);
                        }


                    }
                }
                // console.log("length search res " + len_searchRes)
            }



        }

        if (poiActive){

            setPoiFeatureVisibility();

        }


    }
    // if (floor_layers.length > 0) {
    //     floor_layers[index].setVisible(true);
    //     $("#floor-links li:nth-child(" + (floor_layers.length - index) + ")").addClass("active");
    //
    //     // set active_floor_num
    //     active_floor_num = floor_layers[index].getProperties().floor_num;
    //     if (routeLayer) {
    //         var features = routeLayer.getSource().getFeatures();
    //         for (var i = 0; i < features.length; i++) {
    //             var feature_floor = features[i].getProperties().floor;
    //             if (feature_floor == active_floor_num) {
    //                 features[i].setStyle(route_active_style);
    //             } else {
    //                 features[i].setStyle(route_inactive_style);
    //             }
    //         }
    //     }
    // }
}


function activateLayer(index) {
    hideLayers();
    setLayerVisible(index);
    if (typeof update_url == undefined) {
    // safe to use the function
        update_url('map');
    }else{

    }

}