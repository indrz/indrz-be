// var poiLayer;
var poiLayerName;

var poiLayers = [];


function testCreatePoi(layername) {

    var poiUrl = baseApiUrl + "campus/1/poi/name/" + layername + '/?format=json';

    var source = new ol.source.Vector();

    indrzApiCall(poiUrl).then(function (response) {
        return response.json();
    }).then(function (json) {
        var format = new ol.format.GeoJSON();
        var features = format.readFeatures(json, {featureProjection: 'EPSG:3857'});

        source.addFeatures(features);
    });

    var vectorLayer = new ol.layer.Vector({
        source: source,
        title: layername
    });

    poiLayerGroup.getLayers().push(vectorLayer)

    return vectorLayer;
}


function getLayerGroupByName() {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {

            if(layer.getProperties().id === 99999){

                var poi_groupLayer = layer.getLayers();
                return poi_groupLayer;

            }
        }
    });

}


function disablePoiById(poiId) {
     map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)

            if(layer.getProperties().id === 99999){
                // console.log(layer.getProperties());

                // console.log("Group Name is : " + layer.getProperties().name);


                layer.getLayers().forEach(function (sublayer) {
                    // console.log(sublayer.getProperties().text);
                    // console.log(poiId);


                        if(sublayer.getProperties().id === poiId){
                            // console.log("WOOOOOOOOOW");

                                sublayer.setVisible(false);

                        }
                    });
            }

        }
    });

}



function disableVisibleAllPois(poiId){

  // poiname will be set either to poiname or to false.
  //poiname = poiname || false;




    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)

            if(layer.getProperties().id === 99999){

                // console.log("Group Name is : " + layer.getProperties().name);


                layer.getLayers().forEach(function (sublayer) {
                    // console.log(sublayer.getProperties().id);

                        if(sublayer.getProperties().id === poiId){
                            // console.log("WOOOOOOOOOW");

                                sublayer.setVisible(false);

                        }
                    });
            }

        }
    });

}


function listActivePoiLayers() {

    var poiStatus = false;

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)

            if(layer.getProperties().name === "poi group"){

                // console.log("Group Name is : " + layer.getProperties().name);


                layer.getLayers().forEach(function (sublayer) {
                // map.removeLayer(layer);

                    // console.log("layer name : " + sublayer.getProperties().name);
                    // console.log("layer visibility : " + sublayer.getVisible())

                    });




            }
            else{
                // console.log("no active pois on map");
                return poiStatus;
            }


        }
    });

}

function indrzRemoveLayerById(someId) {
        map.getLayers().forEach(function (layer, i) {

            var lyrProps = layer.getProperties();

            if(lyrProps.id === someId){
                map.removeLayer(layer);
            }else if (lyrProps.layer_id === someId){
                map.removeLayer(layer);

            }

    });



}


function listAllLayers() {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer) {
                // map.removeLayer(layer);

                    // console.log("layer name : " + sublayer.getProperties().name)
                    // console.log("layer visibility : " + sublayer.getVisible())

            });
        }else{
            // console.log(layer.getProperties());
        }
    });

}

function listVisibleLayers() {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer) {

                if (sublayer.getVisible()){
                    // console.log("layer name : " + sublayer.getProperties().name);
                    // console.log("poi floor num: " + sublayer.getProperties().floor_num);
                    // console.log("layer visibility : " + sublayer.getVisible())

                } else{
                    // console.log("not visible")

                }
                // map.removeLayer(layer);



            });
        }
    });

}


function setPoiVisibility(poiId) {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, i) {
                // console.log(sublayer.getProperties().id);

                // map.removeLayer(layer);
                if (sublayer.getProperties().id === poiId) {

                    if(sublayer.getVisible() === true){

                        sublayer.setVisible(false);

                    }
                    else {
                        sublayer.setVisible(true);
                        poiActive = true;
                    }


                }

            });
        }
    });

}

function activatePoiLegend(iconName){

}

function deactivatePoiLegend(iconName){

}


function setPoiStyleOnLayerSwitch(iconName, visible){

    var poiIconImage = '/static/homepage/img/' + iconName + '.png';


    var iconDeactiveStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            opacity: 0.4,
            src: poiIconImage
            // src: '/static/homepage/img/other.png'
        }))
    });

    var iconActiveStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            opacity: 1,
            src: poiIconImage
        }))
    });

    if (visible==true){
        return iconActiveStyle
    }else{
        return iconDeactiveStyle
    }

}

function setPoiFeatureVisibility(){


    // check if poi is already created if so skip and make visible instead
        map.getLayers().forEach(function (layer, i) {

        if (layer instanceof ol.layer.Group) {
            //TODO remove language check de en bad design

            if(layer.getProperties().name === "poi group" || layer.getProperties().name === "POI-Gruppe" ){

            // console.log("Group Name is : " + layer.getProperties().name)
                layer.getLayers().forEach(function (sublayer, i) {

                        // if (sublayer.getProperties().name === poiName) {
                        //         console.log(sublayer.getProperties());


                                sublayer.getSource().forEachFeature(function (feature,i){

                                    if(feature.getProperties().floor_num != active_floor_num){

                                        // console.log(feature.getStyle().getImage().getOpacity());
                                        // console.log(feature.getProperties().fk_poi_category.icon_css_name);
                                        // feature.getStyle().getImage().setOpacity(1);

                                        feature.setStyle(setPoiStyleOnLayerSwitch(feature.getProperties().fk_poi_category.icon_css_name, false));
                                        // console.log(feature.getProperties());

                                    }else{
                                        feature.setStyle(setPoiStyleOnLayerSwitch(feature.getProperties().fk_poi_category.icon_css_name, true));
                                        // console.log(style_active.getImage().getOpacity())
                                    }
                                });

                        // }
                });

            }
        }
    });


}

function poiVisible(poiName){

    var isVisible = false;
    // check if poi is already created if so skip and make visible instead
        map.getLayers().forEach(function (layer, i) {

        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, i) {

                if (sublayer.getProperties().name === poiName) {

                    var poiVisibility = sublayer.getVisible();

                    if (poiVisibility === true){
                        isVisible = true;
                    }else{
                        isVisible = false;
                    }


                }

            });
        }
    });

    return isVisible;

}


function poiExist(poiCatId, poiName){


    poiName = typeof poiName !== 'undefined' ? poiName : 0;

    var itExists = false;
    // check if poi is already created if so skip and make visible instead
        map.getLayers().forEach(function (layer, i) {

        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, i) {
                // console.log(sublayer.getProperties());

                if (sublayer.getProperties().id === poiCatId  || sublayer.getProperties().name === poiName) {
                    itExists = true;

                }

            });
        }
    });

    return itExists;

}


function createPoiStyle(poiIconName, active, floorNum){

    var poiIconImageHidden = '/static/homepage/img/other.png';
    var poiIconImage = '/static/homepage/img/' + poiIconName + '.png';
    var srcImage;
    var mainPoiIcons = ["education_active","access_active","security_active", "infrastructure_active", "services_active"]

    var floorNumber = floorNum.toString();

    var iconDeactiveStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            opacity: 0.4,
            src: poiIconImage
        }))
    });

    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: poiIconImage
        }))
        // ,
        // text: new ol.style.Text({
        //         text: floorNum.toString(),
        //         offsetY: -8,
        //         fill: new ol.style.Fill({
        //           color: '#fff'
        //         })
        //       })

    });

    if (active==='y'){

        if($.inArray(poiIconName, mainPoiIcons) == -1){
            return iconStyle;
        }else{
            return iconDeactiveStyle;
        }


        return iconStyle;
    }
    else {

        return iconDeactiveStyle;
    }

}


var poiDataResp;
var poiCatIdNew;

function findNode(id, currentNode) {


    var i, currentChild, result;

    if (id === currentNode.id) {
        // console.log(currentNode);
        return currentNode;

    } else {

        // Use a for loop instead of forEach to avoid nested functions
        // Otherwise "return" will not work properly

                if(currentNode.hasOwnProperty('nodes')){

                    for (i = 0; i < currentNode.nodes.length; i += 1) {
                    currentChild = currentNode.nodes[i];

                    // console.log(currentChild);

                    // Search in the current child
                    result = findNode(id, currentChild);
                    // console.log(result);

                    if(result.id === id)
                    {
                        // console.log(result.text);

                        return result
                    }

                    // // Return the result if the node has been found
                    if (result !== false) {
                            return result;
                        }
                    }

                }


        // The node has not been found and we have no more options
        return false;
    }


}


function showPoiTree(poiName, poiCatId) {

    poiCatId = poiCatId || 0;

    if (poiCatId !== 0) {

        for(i=0;i<poiCatId.length;i++){

            var currentPoiCatId = poiCatId[i];

            var test = findNode(currentPoiCatId, {"id":-1, "nodes": poiTreeData});

            var x = $('#indrzPoiTree').treeview('search', [test.text, {
                ignoreCase: false,     // case insensitive
                exactMatch: true,    // like or equals
                revealResults: true,  // reveal matching nodes
            }]);

            var poiNodeId = x[0].nodeId;

            if (poiExist(currentPoiCatId) === true) {

                // setPoiVisibility(poiId);
                // console.log("setVisible it EXISTS "+ node.text);

            } else {
                createPoi(1, "", currentPoiCatId);
            }

            $('#indrzPoiTree').treeview('enableNode', [poiNodeId, {silent: true}]);
            $('#indrzPoiTree').treeview('selectNode', [poiNodeId, {silent: true}]);
            $('#indrzPoiTree').treeview('revealNode', [poiNodeId, {silent: true}]);


        }

        $('#collapsePoi').collapse('show');
        $('#indrzPoiTree').treeview('clearSearch');

    } else {

        var d = $('#indrzPoiTree').treeview('search', [poiName, {
            ignoreCase: false,     // case insensitive
            exactMatch: true,    // like or equals
            revealResults: true,  // reveal matching nodes
        }]);

        // d will only ever have one object so get it d[0]

        var poiId = d[0].id;
        var poiNodeId = d[0].nodeId;
        var node = d[0];

        if (poiExist(poiId) === true) {

            // setPoiVisibility(poiId);
            // console.log("setVisible it EXISTS "+ node.text);

        } else {
            // now select all subnodes with a loop
            if (typeof node['nodes'] !== "undefined") {

                var children = node['nodes'];
                // console.log("children " + children);

                for (var i = 0; i < children.length; i++) {

                    $('#indrzPoiTree').treeview('selectNode', [children[i].nodeId, {silent: false}]);

                    if (poiExist(children[i].id) === true) {
                        // setPoiVisibility(children[i].text);
                        //console.log("setVisibility MULTIPLE " + children[i].text);
                    } else {
                        var catId = children[i].id;
                        // var catNumId = Catid.split("_")[1];
                        var poiIconName = children[i].icon;
                        createPoi(1, children[i].text, catId);
                    }
                }
            } else {
                var catId = node.id;
                // var catNumId = Catid.split("_")[1];
                var poiIconName = node.icon;
                // console.log("CREATE POI  " + node.text);
                createPoi(1, node.text, catId);

            }

        }


        $('#collapsePoi').collapse('show');
        $('#indrzPoiTree').treeview('enableNode', [poiNodeId, {silent: true}]);
        $('#indrzPoiTree').treeview('selectNode', [poiNodeId, {silent: true}]);
        $('#indrzPoiTree').treeview('revealNode', [poiNodeId, {silent: true}]);
        $('#indrzPoiTree').treeview('clearSearch');


    }


}


function showSinglePoi(poiId, zlevel) {

    globalPopupInfo.poiId = poiId;

    if(poiSingleLayer){
        map.removeLayer(poiSingleLayer)

    }

    var poi_title = "";

    //http://localhost:8000/indrz/api/v1/campus/1/poi/251/

    var poiUrl = baseApiUrl + "campus/1/poi/" + poiId + '/?format=json';


    // create the poi because it does not exist
    var poiSource = new ol.source.Vector();

    indrzApiCall(poiUrl).then(function (response) {
        // console.log("in response: " + response);
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        poiSource.addFeatures(featuresSearch);


        var centerCoord = ol.extent.getCenter(poiSource.getExtent());

        if (featuresSearch.length === 1) {

            var offSetPos = [0,-35];

            var poi_properties = featuresSearch[0].getProperties()
            poi_properties.poiId = poiId;

            open_popup(poi_properties, centerCoord, -1, offSetPos);

            zoomer(centerCoord, zlevel);

            globalPopupInfo.poiCatId = featuresSearch[0].getProperties().fk_poi_category.id;
            globalPopupInfo.poiCatShareUrl = "?poi-cat-id=" + featuresSearch[0].getProperties().fk_poi_category.id;
        }

    });

    var poiSingleLayer = new ol.layer.Vector({

        source: poiSource,
        // style: createPoiStyle(poiIconName, 'y'),
        style: function (feature, resolution) {

            var poiFeature_floor = feature.getProperties().floor_num;

            if (req_locale === "de"){
                poi_title = feature.getProperties().name_de;

            }else{poi_title
                poi_title = feature.getProperties().name;
            }

            var css_name = feature.getProperties().fk_poi_category.icon_css_name;

            // feature.setStyle(createPoiStyle(css_name, 'y', poiFeature_floor));

            if (poiFeature_floor == active_floor_num) {
                feature.setStyle(createPoiStyle(css_name, 'y', poiFeature_floor));
            } else {            var poiFooId = "";
		    if(feature){
		            poiFooId = feature.getId();


		    }
                feature.setStyle(createPoiStyle(css_name, 'n', poiFeature_floor));
            }
        },

        title: poi_title,
        name: poi_title,
        id: poiId,
        active: true,
        visible: true,
        zIndex: 999
    });

    map.addLayer(poiSingleLayer);



}

function hideSinglePoiLayer() {

    map.removeLayer(sPoiLyr);

    map.getLayers().forEach(function (layer, i) {
        var props = layer.getProperties();

        if (props.id === poiSingleLayer.get('id')){
            layer.setVisible(false);

        }

    });

}

function createPoi(campusId, poiName, poiCatId, poiIconName) {
    poiActive = true;
    var poi_title = "";

    if (poiExist(poiCatId)){
        // do nothing

    } else {

        var poiUrl = baseApiUrl + "campus/1/poi/poi/cat/" + poiCatId + '/?format=json';


        // create the poi because it does not exist
        var poiSource = new ol.source.Vector();

            var floor_num, poi_name, cat_name, icon_name, icon_geom;

        indrzApiCall(poiUrl).then(function (response) {
            // console.log("in response: " + response);
            var geojsonFormat3 = new ol.format.GeoJSON();
            var featuresSearch = geojsonFormat3.readFeatures(response,
                {featureProjection: 'EPSG:4326'});
            poiSource.addFeatures(featuresSearch);

        });

        var poiVectorLayer = new ol.layer.Vector({



            source: poiSource,
            // style: createPoiStyle(poiIconName, 'y'),
            style: function (feature, resolution) {

                var poiFeature_floor = feature.getProperties().floor_num;

                if (req_locale === "de"){
                    poi_title = feature.getProperties().name_de;

                }else{
                    poi_title = feature.getProperties().name;
                }

                var css_name = feature.getProperties().fk_poi_category.icon_css_name;

                // feature.setStyle(createPoiStyle(css_name, 'y', poiFeature_floor));

                // TODO on floor level change update poi icons
                //  this CODE WORKS below but MUST also be updated on floor level change
                if (poiFeature_floor == active_floor_num) {
                    feature.setStyle(createPoiStyle(css_name, 'y', poiFeature_floor));
                } else {
                    feature.setStyle(createPoiStyle(css_name, 'n', poiFeature_floor));
                }
            },

            title: poi_title,
            name: poi_title,
            id:poiCatId,
            active: true,
            visible: true,
            zIndex: 999
        });

        poiLayerGroup.getLayers().push(poiVectorLayer);

        return poiVectorLayer;
    }


}


$('#kiosk-pois a').click(function() {

    var poiCatName = $(this).attr('id').split('_')[0];
    var poiCatId = $(this).attr('id').split('_')[1];
    var poiIconName = $('#kiosk-pois a > img').attr('class');
    var poiIconName = $(this).attr('aria-label');

    if (poiExist(poiCatId)){

        setPoiVisibility(poiCatId);
        $(poiCatId).addClass("active");

    }
    else {
        var newPoi = createPoi(1,poiCatName, poiCatId, poiIconName);
        map.getLayers().push(newPoi);

    }


});

