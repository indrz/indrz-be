(function loadMatomo () {
  const _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function () {
    const u = 'https://yourwebsite.com/';
    _paq.push(['setTrackerUrl', u + 'piwik.php']);
    _paq.push(['setSiteId', '137']);
    const d = document; const g = d.createElement('script'); const s = d.getElementsByTagName('script')[0];
    g.type = 'text/javascript'; g.async = true; g.src = u + 'piwik.js'; s.parentNode.insertBefore(g, s);
  })();
})();
