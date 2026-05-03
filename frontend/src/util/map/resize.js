export const handleWindowResize = (mapId) => {
  const headerEl = document.getElementById('indrz-header-container');
  const footerEl = document.getElementById('indrz-footer-container');
  const headerHeight = headerEl ? headerEl.offsetHeight : 0;
  const footerHeight = footerEl ? footerEl.offsetHeight : 0;
  const mapContainer = document.getElementById(mapId);

  if (!mapContainer) {
    return;
  }

  mapContainer.style.height = window.innerHeight - (headerHeight + footerHeight) + 'px';
};

