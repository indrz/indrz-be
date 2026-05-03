<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
<sld:NamedLayer>
  <sld:Name>indrz-building-</sld:Name>
  <sld:UserStyle>
    <sld:Name>indrz-building</sld:Name>
    <sld:Title>Default polygon style</sld:Title>
    <sld:Abstract>A sample style that just draws out a solid gray interior with a black 1px outline</sld:Abstract>
    <sld:FeatureTypeStyle>
      <sld:Name>name</sld:Name>
      <sld:Rule>
        <sld:Name>Building</sld:Name>
        <sld:MinScaleDenominator>1000.0</sld:MinScaleDenominator>
        <sld:MaxScaleDenominator>7900.0</sld:MaxScaleDenominator>
        <sld:TextSymbolizer>
          <sld:Geometry>
            <ogc:Function name="centroid">
              <ogc:PropertyName>geom</ogc:PropertyName>
            </ogc:Function>
          </sld:Geometry>
          <sld:Label>
            <ogc:PropertyName>name</ogc:PropertyName>
          </sld:Label>
          <sld:Font>
            <sld:CssParameter name="font-family">Arial Black</sld:CssParameter>
            <sld:CssParameter name="font-size">14</sld:CssParameter>
            <sld:CssParameter name="font-style">normal</sld:CssParameter>
            <sld:CssParameter name="font-weight">bold</sld:CssParameter>
          </sld:Font>
          <sld:LabelPlacement>
            <sld:PointPlacement>
              <sld:AnchorPoint>
                <sld:AnchorPointX>0.5</sld:AnchorPointX>
                <sld:AnchorPointY>0.5</sld:AnchorPointY>
              </sld:AnchorPoint>
            </sld:PointPlacement>
          </sld:LabelPlacement>
          <sld:Fill>
            <sld:CssParameter name="fill">#FFFFFF</sld:CssParameter>
          </sld:Fill>
          <sld:Graphic>
            <sld:Mark>
              <sld:WellKnownName>circle</sld:WellKnownName>
              <sld:Fill>
                <sld:CssParameter name="fill">#04799c</sld:CssParameter>
                <sld:CssParameter name="fill-opacity">0.7</sld:CssParameter>
              </sld:Fill>
                            <sld:Stroke>
                <sld:CssParameter name="stroke">#a6a6a6</sld:CssParameter>
              </sld:Stroke>
            </sld:Mark>
            <Size>38</Size>
          </sld:Graphic>

          <sld:VendorOption name="graphic-margin">2</sld:VendorOption>
          <sld:VendorOption name="goodnessOfFit">5</sld:VendorOption>
          <sld:VendorOption name="conflictResolution">false</sld:VendorOption>
          <sld:VendorOption name="repeat">1</sld:VendorOption>

        </sld:TextSymbolizer>
      </sld:Rule>



    </sld:FeatureTypeStyle>
  </sld:UserStyle>
</sld:NamedLayer>
</sld:StyledLayerDescriptor>
