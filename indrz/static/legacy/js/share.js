$('#ShareMapModal').on('shown.bs.modal', function () {
  update_url('map')
  $('.share-link').val(location.href)
  $('.share-link').focus()
  $('.share-link').select()
})

$('#ShareRouteModal').on('shown.bs.modal', function () {
  update_url('route')
  $('.share-link').val(location.href)
  $('.share-link').focus()
  $('.share-link').select()
})

$('#ShareSearchModal').on('shown.bs.modal', function () {

  if (globalPopupInfo.hasOwnProperty('wmsInfo')) {

    if (globalPopupInfo.wmsInfo) {
      update_url('wmsInfo')
      $('.share-link').val(location.href)
      $('.share-link').focus()
      $('.share-link').select()
    }

  }

  if (globalSearchInfo.searchText) {
    update_url('search')
    $('.share-link').val(location.href)
    $('.share-link').focus()
    $('.share-link').select()

  }

})

$('#sharePoiModal').on('shown.bs.modal', function () {
  update_url('poiCatId')
  $('.share-link').val(location.href)
  $('.share-link').focus()
  $('.share-link').select()
})

