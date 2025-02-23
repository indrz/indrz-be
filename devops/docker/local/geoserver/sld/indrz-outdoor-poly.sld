<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>generic</Name>
    <UserStyle>
      <Title>Generic</Title>
      <Abstract>Generic style</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Title>Pflanzen</Title>
          <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>pflanzen</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>

          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#92d179</CssParameter>
              <CssParameter name="fill-opacity">0.5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#92d179</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

        <Rule>
          <Title>baum</Title>
          <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>baum</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>

          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#74a760</CssParameter>
              <CssParameter name="fill-opacity">0.5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#74a760</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

        <Rule>
          <Title>moebel</Title>
          <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>moebel</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>

          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#CD853F</CssParameter>
              <CssParameter name="fill-opacity">0.5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#CD853F</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Title>other</Title>
          <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>other</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>

          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#D3D3D3</CssParameter>
              <CssParameter name="fill-opacity">0.5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#D3D3D3</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


        <VendorOption name="ruleEvaluation">first</VendorOption>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>