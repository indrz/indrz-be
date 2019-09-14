$(function () {
    // 6 create an instance when the DOM is ready
    $('#jstree').jstree({
        "checkbox": {
            "keep_selected_style": true,
            "visible": false,
            "three_state": true,
            "cascade": "down"
        },
        "plugins": ["checkbox", "wholerow"]
    });


    // $('#jstree').on("changed.jstree", function (e, data) {
    //     var nodeName = $('#jstree').jstree(true).get_text(data.node);
    //     var poiName = nodeName.trim();
    //     if (poiExist(poiName)) {
    //
    //     }
    //     else {
    //         var Catid = data.node.id;
    //         var catNumId = Catid.split("_")[1];
    //         var poiIconName = $('#jstree').jstree(true).get_icon(data.node.id);
    //         createPoi(1, poiName, catNumId, poiIconName.replace('_active', ''));
    //     }
    //
    // });


    $("#jstree")
        .on('select_node.jstree', function (evt, data) {

            var nodeName = $('#jstree').jstree(true).get_text(data.node.id);
            var poiIconName2 = $('#jstree').jstree(true).get_icon(data.node.id);

            var poiName = nodeName.trim();


            if($('#jstree').jstree(true).is_parent(data.node.id)){
                // this is a parent node was clicked
                console.log($('#jstree').jstree(true).is_selected(data.node.id));
                console.log($('#jstree').jstree(true).is_parent(data.node.id));
                console.log($('#jstree').jstree(true).is_open(data.node.id));
                console.log($('#jstree').jstree(true).is_leaf(data.node.id));
                console.log($('#jstree').jstree(true).get_children_dom(data.node.id));
                // var f = $('#jstree').jstree(true).get_json(data.node.id);
                // console.log(JSON.stringify(f));
                //
                // data.instance.set_icon(data.node, poiIconName2 + '_active');

            }

            $( "#jstree" ).each(function( index ) {
              // console.log( index + ": " + $( this ).text() );
            });


            if (poiExist(poiName)) {
                setPoiVisibility(poiName);
                data.instance.set_icon(data.node, poiIconName2 + '_active');

            } else {


                var Catid = data.node.id;
                var catNumId = Catid.split("_")[1];
                var poiIconName = $('#jstree').jstree(true).get_icon(data.node.id);
                createPoi(1, poiName, catNumId, poiIconName2.replace('_active', ''));
                data.instance.set_icon(data.node, poiIconName2 + '_active');
            }


        })
        .on('deselect_node.jstree', function (evt, data) {

            var nodeName = $('#jstree').jstree(true).get_text(data.node.id);
            var poiIconName3 = $('#jstree').jstree(true).get_icon(data.node.id);

            data.instance.set_icon(data.node, poiIconName3.replace("_active", ""));

            setPoiVisibility(nodeName.trim());

        });


});

//
// var OKtoCascadeUp = 0;
// var OKtoCascadeDown = 0;
//
// function CascadeUp(inNode, inCommand) {
//     if (OKtoCascadeUp < 1) {
//         ParentNode = $('#jstree').jstree('get_parent', inNode);
//         $('#jstree').jstree(inCommand, ParentNode);
//     }
// }
//
// function CascadeDown(inNode, inCommand) {
//     if (OKtoCascadeDown < 1) {
//         ChildrenNodes = jQuery.makeArray($('#jstree').jstree('get_children_dom', inNode));
//         $('#jstree').jstree(inCommand, ChildrenNodes);
//     }
// }


// $(function () {
//
//     // Setup tree (http://www.jstree.com/)
//     // $('#jstree').jstree({
//     //     'plugins': ['checkbox'],
//     //         'checkbox': {
//     //         'keep_selected_style': false,
//     //             'three_state': false,
//     //             'cascade': ''
//     //     }
//     // });
//
//     // Initialize tree
//     $('#jstree').jstree('hide_icons');
//     $('#jstree').jstree('select_all');
//     $('#jstree').jstree('open_all');
//
//     // Selection Actions
//     $('#jstree').on("select_node.jstree", function (e, data) {
//         $('#jstree').jstree('open_node', data.node);
//         OKtoCascadeDown++;
//         CascadeUp(data.node, 'select_node');
//         OKtoCascadeDown--;
//         CascadeDown(data.node, 'open_node');
//         CascadeDown(data.node, 'select_node');
//     });
//
//     // Deselection Actions
//     $('#jstree').on("deselect_node.jstree", function (e, data) {
//         $('#jstree').jstree('open_node', data.node); //need this to have it deselect hidden nodes
//         CascadeDown(data.node, 'open_node');
//         CascadeDown(data.node, 'deselect_node');
//         CascadeDown(data.node, 'close_node');
//         $('#jstree').jstree('close_node', data.node); //need this to have it deselect hidden nodes
//     });
//
// });