var roomNums = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: 'http://localhost:8000/api/v1/spaces/?format=json'
});

// passing in `null` for the `options` arguments will result in the default
// options being used
$('#rooms-prefetch .typeahead').typeahead(null, {
    name: 'countries',
    limit: 100,
    source: roomNums
});


$("#submitForm").submit(function (event) {
    {#  alert( "Handler for .submit() called."  );#}
    var startNum = $('#route-from').val();
    var endNum = $('#route-to').val();
    var rType = $("input:radio[name=typeRoute]:checked").val();
    addRoute(startNum, endNum, rType);
    event.preventDefault();
});/**
* Created by mdiener on 16.11.2015.
*/
