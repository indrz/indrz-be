function createMapPNG() {

    map.once('postcompose', function (event) {
        var canvas = event.context.canvas;
        var curDate = new Date();

        /* ... your canvas manipulations ... */
        if (canvas.toBlob) {
            canvas.toBlob(
                function (blob) {
                    // Do something with the blob object,
                    // e.g. creating a multipart form for file uploads:
                    saveAs(blob, curDate.toLocaleDateString() + '_AAU-map.png');
                    /* ... */
                },
                'image/png'
            );
        }

    });
    map.renderSync();

}

function getMapSize() {
    var mapSizePixels = map.getSize()[0] - map.getSize()[1];
    // console.log("map Size in Pix: " + mapSizePixels);

    var mapWidthPixels = map.getSize()[0];
    // console.log("width pix: " + mapWidthPixels);
    var mapHeightPixels = map.getSize()[1];
    // console.log("height pix: " + mapHeightPixels);
    var mapExtent = map.getView().calculateExtent(map.getSize());
    // console.log("map extent pix: " + mapExtent);
    var xScreenDist = mapExtent[2] - mapExtent[0];
    // console.log("xScreenDist: " + xScreenDist);
    var pxPerMeter = map.getView().getResolution(); // resoltuion is is the size of 1 pixel in map units
    // console.log("px per meter: " + pxPerMeter);
    var scaleVal = mapWidthPixels * pxPerMeter;
    // console.log("scale val: " + scaleVal);

    var foorss = mapWidthPixels / 200;
    var newwidth = mapWidthPixels / foorss;
    // console.log("width in mm: " + newwidth);

    var newheight = mapHeightPixels / foorss;
    // console.log("new height is : " +  newheight);

    return {
        "width_px": mapWidthPixels,
        "height_px": mapHeightPixels,
        "new_width": newwidth,
        "new_height": newheight
    }

}


function getBase64Image(img) {
    var canvas = document.createElement("canvas");

    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, 50, 30);
    var dataURL = canvas.toDataURL("image/png");
    // return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    return dataURL;
}


function calculateAspectRatioFit(srcWidth, srcHeight, maxWidth, maxHeight) {

    var ratio = Math.min(maxWidth / srcWidth, maxHeight / srcHeight);

    return {
        width: srcWidth * ratio,
        height: srcHeight * ratio
    };
}


function map2pdf() {

    map.once('postcompose', function (event) {
        var canvas = event.context.canvas;
        var mapSize = getMapSize();

        var canvasMapHeight = mapSize.height_px;
        var canvasMapWidth = mapSize.width_px;

        var ratio = canvasMapHeight / canvasMapWidth;
        var ratio_portrait = canvasMapWidth / canvasMapHeight;

        var page_orientation = "landscape";

        if (ratio > 1) {
            page_orientation = "portrait";
        }

        var mm_r = 72 / 25.4; // 2,833
        var px_r = 96 / 72; // 1,3333



        // var wulogo_dataurl = getBase64Image(document.getElementById("wulogo"));

        // var wulogo_dataurl = getBase64Image("https://www.opendataportal.at/wp-content/uploads/2016/09/WU-Wien-Logo.png");

        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1; //January is 0!

        var yyyy = today.getFullYear();
        if (dd < 10) {
            dd = '0' + dd;
        }
        if (mm < 10) {
            mm = '0' + mm;
        }
        var today = dd + '.' + mm + '.' + yyyy;
        var todayFileName = yyyy + '-' + mm + '-' + dd;

        if (canvas.toBlob) {
            canvas.toBlob(
                function (blob) {
                    // Do something with the blob object,
                    // e.g. creating a multipart form for file uploads:
                    var doc = new jsPDF({
                        orientation: page_orientation,
                        unit: 'px',
                        //format: [210, 297]  // height, width
                        format: 'a4' // w 595.28, h 841.89  portrait
                    });

                    var pdfWidth = doc.internal.pageSize.width;
                    var pdfHeight = doc.internal.pageSize.height;

                    var maxWidth = pdfWidth;
                    var maxHeight = pdfHeight;

                    var pdfLeftMargin = 20;
                    var pdfRightMargin = 20;
                    var pdfTopMargin = 40;
                    var pdfBottomMargin = 20;

                    if (ratio > 1) {
                        // portrait
                        maxWidth = pdfWidth - pdfLeftMargin - pdfRightMargin;
                        maxHeight = pdfHeight - pdfTopMargin - pdfBottomMargin;
                    } else {
                        maxWidth = pdfWidth - pdfLeftMargin - pdfRightMargin;
                        maxHeight = pdfHeight - pdfTopMargin - pdfBottomMargin;

                    }


                    var pdfMapWidth = pdfWidth - (pdfLeftMargin + pdfRightMargin);
                    var pdfMapHeight = pdfHeight - pdfTopMargin - pdfBottomMargin;


                    var title_x_pos = pdfMapWidth / 2.4;
                    var title_y_pos = 25;

                    // console.info("doc width height is: " + pdfWidth, pdfHeight);
                    // console.info("image width height is: " + canvasMapWidth, canvasMapHeight);
                    // console.log("image port width height is: " + new_port_img_w + " " + new_port_img_h);
                    // console.log("image land width height is: " + new_land_img_w + " " +  new_land_img_h);
                    // console.info("ration-portrait " + ratio_portrait);
                    // console.info('ratio-landscape ' + ratio);
                    // console.info("div ie canvas width and height " + canvasMapWidth + " " + canvasMapHeight);
                    // console.info("canvas ratio: " + ratio);

                    doc.setFont('Arial');

                    doc.setFontSize(22);

                    doc.text('AAU Campus Plan', title_x_pos, title_y_pos);
                    doc.setFontSize(12);

                    var x = calculateAspectRatioFit(canvasMapWidth, canvasMapHeight, maxWidth,
                        maxHeight);
                    // console.log("great test: w " + x.width);
                    // console.log("great test: h"+ x.height);


                    var urlCreator = window.URL || window.webkitURL;
                    var imageUrl = urlCreator.createObjectURL(blob);
                    // document.querySelector("#image").src = imageUrl;

                    var reader = new window.FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = function () {
                        base64data = reader.result;
                        // console.log(base64data );
                        //portrait
                        if (ratio > 1) {
                            var pdfLeftMargin = (pdfWidth - x.width) / 2;
                            doc.text("Stockwerk:  " + active_floor_num, 208, title_y_pos + 10);
                            doc.addImage(base64data, 'PNG', pdfLeftMargin, 40, x.width, x
                                .height);
                            doc.text(today, 20, 617);

                            // doc.addImage(wulogo_dataurl, 'png', title_x_pos-30, title_y_pos-4, 15, 10);

                        } else {
                            var pdfLeftMargin = (pdfWidth - x.width) / 2;
                            doc.text("Stockwerk:  " + active_floor_num, 300, title_y_pos + 10);
                            doc.addImage(base64data, 'PNG', pdfLeftMargin, 40, x.width, x
                                .height);
                            doc.text(today, 20, 420);
                            // doc.addImage(wulogo_dataurl, 'png', title_x_pos-30, title_y_pos-4, 15, 10);
                        }


                        doc.save(todayFileName + '-WU-Plan.pdf')


                    }
                    /* ... */
                },
                'image/jpeg'
            );
        }



    });

    map.renderSync();

}


$('#id-export-png').on('click', function () {


    createMapPNG();

});


$('#id-export-pdf').on('click', function () {
    // mapScreenshot();
    // createPrintRequest();
    map2pdf();
    // getMapSize();
});