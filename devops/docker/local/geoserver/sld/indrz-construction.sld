<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
                       xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd"
                       xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <NamedLayer>
    <Name>indrz-construction</Name>
    <UserStyle>
      <Title>A rosa polygon style</Title>
      <FeatureTypeStyle>
        <Rule>
          <Title>rosa</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>short_name</ogc:PropertyName>
              <ogc:Literal>Construction</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#f5e5ef
              </CssParameter>
              <CssParameter name="fill-opacity">0.9
              </CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#f5e5ef</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>

        </Rule>

        <Rule>
          <Title>Construction icon</Title>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>short_name</ogc:PropertyName>
              <ogc:Literal>Construction</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <MaxScaleDenominator>2100</MaxScaleDenominator>


          <PointSymbolizer>
            <Geometry>
              <ogc:Function name="centroid">
                <ogc:PropertyName>geom</ogc:PropertyName>
              </ogc:Function>
            </Geometry>
            <Graphic>
              <ExternalGraphic>
                <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="construction_32.png"/>
                <Format>image/png</Format>

              </ExternalGraphic>
              <Size>32</Size>
            </Graphic>

          </PointSymbolizer>

        </Rule>

      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
