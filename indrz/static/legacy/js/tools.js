if (typeof console === "undefined" || console.log === undefined || console.info === undefined || console.error === undefined) {
    var console =
    {
        log: function () {
        },
        info: function () {
        },
        error: function () {
        }
    };
}

function indrzGetJson(geoJsonUrl){
    return $.getJSON( geoJsonUrl, function(data) {
      // console.log( "success" );
    })
      .done(function(data) {

      })
      .fail(function() {
        console.log( "error getting json from url" + geoJsonUrl );
      });
}


function getResultFromURL(url) {
    var retStr = "";

    $.ajax({
        url: url,
        success: function (response) {
            retStr = response;
        },
        error: function (e) {
            res = null;
            console.error("Failed to call " + url);
        },
        async: false,
        timeout: 7500 // 7.5 seconds
    });

    return retStr;
}

function indrzApiCall(url, callback) {

    var respObj = $.ajax({
        url: url,
        beforeSend: function (xhr) {
                /* Authorization header */
                xhr.setRequestHeader("Authorization", indrzApiToken );
                xhr.setRequestHeader("X-Mobile", "false");
            },
        //data: JSON.stringify(data),
        //data: data,
        // type: 'POST',
        dataType: "json",
        // contentType: 'application/json; charset=UTF-8',
        success: function (jsonObj) {
            // callback(jsonObj);
        },
        error: function (e) {
            // console.error("Failed to do json rpc call to " + url );
            // callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });

    return respObj;
}



function jsonRpcCall(url, methodName, parameters, callback) {
    data = '{"method": "' + methodName + '", "id": "labla", "params": [' + parameters + '], "jsonrpc":"2.0"}';

    jQuery.ajax({
        url: url,
        //data: JSON.stringify(data),
        data: data,
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success: function (jsonObj) {
            callback(jsonObj.result);
        },
        error: function (e) {
            console.error("Failed to do json rpc call to " + url + " with methodName " + methodName);
            callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });
}

function getResultFromURLWithCallback(url, callback) {

    jQuery.ajax({
        url: url,
        success: function (response) {
            callback(response);
        },
        error: function (e) {
            console.error("Failed to call " + url);
            callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });

}
