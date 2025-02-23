<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>Cartolines</Name>
    <UserStyle>
      <Name>Cartolines</Name>
      <Title>Cartolines</Title>
      <Abstract>Cartolines</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Title>All Cartolines grey</Title>
          <MaxScaleDenominator>2100</MaxScaleDenominator>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="stroke">#797979</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
              <CssParameter name="opacity">0.75</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
