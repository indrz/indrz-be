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
        <MinScaleDenominator>2800</MinScaleDenominator>
        <MaxScaleDenominator>10000000</MaxScaleDenominator>


        <TextSymbolizer>
          <sld:Geometry>
            <ogc:Function name="centroid">
              <ogc:PropertyName>geom</ogc:PropertyName>
            </ogc:Function>
          </sld:Geometry>
          <Label>
            <ogc:PropertyName>name</ogc:PropertyName>
          </Label>
          <Font>
            <CssParameter name="font-family">Bitstream Vera Sans</CssParameter>
            <CssParameter name="font-size">22</CssParameter>
            <CssParameter name="font-color">#797979</CssParameter>
            <CssParameter name="font-weight">bold</CssParameter>
          </Font>
          <LabelPlacement>
            <PointPlacement>
              <AnchorPoint>
                <AnchorPointX>0.5</AnchorPointX>
                <AnchorPointY>0.5</AnchorPointY>
              </AnchorPoint>
              <Displacement>
                <DisplacementX>0</DisplacementX>
                <DisplacementY>0</DisplacementY>
              </Displacement>
            </PointPlacement>
          </LabelPlacement>
          <Fill>
            <CssParameter name="fill">#FFFFFF</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Fill>

          <Graphic>
            <Mark>
              <WellKnownName>circle</WellKnownName>
              <Fill>
                <CssParameter name="fill">#006699</CssParameter>

              </Fill>
              <Stroke>
                <CssParameter name="stroke">#FFFFFF</CssParameter>
                <CssParameter name="stroke-width">1</CssParameter>
              </Stroke>

            </Mark>

          </Graphic>
          <VendorOption name="graphic-resize">proportional</VendorOption>
          <VendorOption name="graphic-margin">8</VendorOption>
          <VendorOption name="goodnessOfFit">0</VendorOption>
          <VendorOption name="conflictResolution">true</VendorOption>
          <VendorOption name="repeat">0</VendorOption>

          <!--



            <VendorOption name="repeat">1</VendorOption>

            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
        </TextSymbolizer>
        </sld:Rule>


    </sld:FeatureTypeStyle>
  </sld:UserStyle>
</sld:NamedLayer>
</sld:StyledLayerDescriptor>