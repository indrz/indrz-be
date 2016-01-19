$('#ShareModal').on('shown.bs.modal', function () {
    $("#id-share-link").val(location.href);
    $("#id-share-link").focus();
    $("#id-share-link").select();
});