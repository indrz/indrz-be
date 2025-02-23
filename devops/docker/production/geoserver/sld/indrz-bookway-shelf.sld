<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
  <NamedLayer>
    <Name>Library Shelf</Name>
    <UserStyle>
      <Name>Library Shelf</Name>
      <Title>Default polygon style</Title>
      <Abstract>Library shelf style</Abstract>
      <FeatureTypeStyle>
        <Name>Shelf</Name>
        <Rule>
          <Name>Shelf scale</Name>
          <Title>Shelf</Title>
          <MaxScaleDenominator>800</MaxScaleDenominator>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#3399FF</CssParameter>
                            <CssParameter name="fill-opacity">0.5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#3366CC</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>