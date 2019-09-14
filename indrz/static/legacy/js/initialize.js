$(document).ready(function () {

    var triggeredResized = false;



    function loadLibraryRoute(){



    }


    function getTree(langCode) {

            indrzApiCall(hostUrl +  langCode + "/indrz/api/v1/campus/1/poi/jstree/?format=json").done(function (json) {

                $('#indrzPoiTree').treeview({
                    levels: 2,
                    color: "#000000",
                    expandIcon: 'fa fa-chevron-right',
                    collapseIcon: 'fa fa-chevron-down',
                    hideCheckbox: true,
                    selectedIcon: '',
                    nodeIcon: '',
                    multiSelect: true,
                    data: json
                });

                poiTreeData = json;


                $('#indrzPoiTree').on('nodeSelected', function (e, node)
                {

                   if (poiExist(node.id)===true) {

                        setPoiVisibility(node.id);
                        // console.log("setVisible it EXISTS "+ node.text);

                   } else{
                        // now select all subnodes with a loop
                        if (typeof node['nodes'] !== "undefined" && node['nodes'] !== "") {

                            var children = node['nodes'];

                            for (var i = 0; i < children.length; i++) {

                                $('#indrzPoiTree').treeview('selectNode', [children[i].nodeId, {silent: false}]);

                                if (poiExist(children[i].id)===true) {
                                    // setPoiVisibility(children[i].text);
                                    //console.log("setVisibility MULTIPLE " + children[i].text);
                                } else {
                                    var catId = children[i].id;
                                    // var catNumId = Catid.split("_")[1];
                                    var poiIconName = children[i].icon;
                                    createPoi(1, children[i].text, catId);
                                }
                            }
                        }else{
                            var catId = node.id;
                            // var catNumId = Catid.split("_")[1];
                            var poiIconName = node.icon;
                            // console.log("CREATE POI  " + node.text);
                            createPoi(1, node.text, catId);

                        }

                    }


                });

                $('#indrzPoiTree').on('nodeUnselected', function (e, node) {


                    if (typeof node['nodes'] !== "undefined") {
                        var children = node['nodes'];
                        for (var i = 0; i < children.length; i++) {

                            $('#indrzPoiTree').treeview('unselectNode', [children[i].nodeId, {silent: true}]);

                                disablePoiById(children[i].id);

                        }
                    }else{
                        // single item in poi with no subnodes
                                disablePoiById(node.id);

                    }
                });


                if(poi_cat_name !== 'undefined' && poi_cat_name !== '' && poi_cat_name !== "none"){

                    showPoiTree(poi_cat_name);

                }

                if(poi_cat_id !== 'undefined' && poi_cat_id !== '' && poi_cat_id !== "noid"){


                    showPoiTree("", poi_cat_id);
                    globalPopupInfo.poiCatId = poi_cat_id;
                    // globalPopupInfo.poiCatShareUrl = "?poi-cat-id=" + globalPopupInfo.poiCatId;


                }




                // Some logic to retrieve, or generate tree structure
                // return json;
            })
                .fail(function () {
                    // console.log("error");
                })
                .always(function () {
                    // console.log("complete");
                    if (!triggeredResized) {
                        triggeredResized = true;
                        setTimeout(function () {
                            $(window).trigger('resize');
                        }, 500);
                    }
                });

        }




    function loadShare(){
        if(search_text !== '' && search_text.length > 3){
            searchIndrz(1, search_text, zoom_level)

        }

    }

    function initialize() {

        // console.log(req_locale);
        // console.log(poi_cat_name);

        //
        if (centerx != 0 && centery != 0 && isNaN(centerx) == false) {
                var view = map.getView();
                view.animate({zoom: zoom_level}, {center: [centerx, centery]});

            }
        //
        // // if(poi_id != 0){
        // //     searchIndrz(1, search_string)
        // //         // map.getLayers().push(spaceLayer);
        // // }
        // //

        //
        //
        if (floor_layers.length > 0) {

            if (route_from !== '' && route_to !== '') {

                initRoute(route_from, route_to);
                // searchForRoute(route_from, route_to);

                $("#route-from").val(route_from);
                $("#route-to").val(route_to);
                // $("#directionsForm").submit();
                $('#collapseRouting').collapse('show'); // open the accordian point routing
                setTimeout(function () {
                    $('#collapsePoi').collapse('hide');
                }, 500);
            } else if (centerx != 0 && centery != 0 && isNaN(centerx) == false) {
                var view = map.getView();
                view.animate({zoom: zoom_level}, {center: [centerx, centery]});

            }
            if (library_key !== 'nokey') {
                library_book_position(library_key);
            }
        } else {
            setTimeout(initialize, 250);
        }

    }

    initialize();
    loadShare();
    getTree(req_locale);

  if (route_from_xyz !== '' && route_to_xyz !== '') {
    $.when(getDirections2(route_from_xyz, route_to_xyz, route_type, 'coords')).then(function (a, b) {
      $('#route-from').val(route_from_xyz)
      $('#route-to').val(route_to_xyz)
      $('#collapseRouting').collapse('show')
      $('#collapsePoi').collapse('hide')
      $('#collapseCampus').collapse('hide')

    })

  }

  if (route_from_spaceid !== '0' && route_to_spaceid !== '0') {
    $.when(getDirections2(route_from_spaceid, route_to_spaceid, route_type, 'spaceIdToSpaceId')).then(function (a) {

    })
  }


  //   if (poi_start_id !== '0' && route_to_spaceid !== '0' && poi_start_id !== -1) {
  //   $.when(getDirections2(route_to_spaceid, poi_start_id,  route_type, 'spaceIdToPoiId')).then(function (a) {
  //
  //   })
  // }




    if(poi_start_id !== "-1" && poi_end_id !== "-1"){
        routeToPoiFromPoi(poi_start_id, poi_end_id);
        // globalRouteInfo.routeUrl = hostUrl + req_locale +"/?start-poi-id=" + poi_start_id + "&end-poi-id=" + poi_end_id
    }

            // if(document.location.href.split('?')[1] != null){
			// 	if(document.location.href.split('?')[1].split("key=")[1] != null){
			// 		var key = document.location.href.split('?')[1].split("key=")[1].split("&")[0];
			// 		// calculateLibraryRoute(key);
			// 		library_book_position(decodeURIComponent(key));
			// 	}
			// }





    if(poi_id !== 'undefined' && poi_id !== '' && poi_id !== "none"){
        showSinglePoi(poi_id, zoom_level);
        globalPopupInfo.poiId = poi_id;


    }





    //calculateLibraryRoute("ST 261.w34 G744");



});

