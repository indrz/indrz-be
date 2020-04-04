<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>wing points</Name>
    <UserStyle>
      <Name>wing points</Name>
      <Title>Default polygon style</Title>
      <Abstract>A sample style that just draws out a solid gray interior with a black 1px outline</Abstract>
      <FeatureTypeStyle>
        <Name>level 1</Name>
        <Rule>
          <Name>level 1</Name>
          <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>category_id</ogc:PropertyName>
              <ogc:Literal>81</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>
           <MinScaleDenominator>2800</MinScaleDenominator>
          <MaxScaleDenominator>100000</MaxScaleDenominator>


          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>name</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">TU Text Medium</CssParameter>
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
            <VendorOption name="repeat">1</VendorOption>

            <!--



            <VendorOption name="repeat">1</VendorOption>

            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>

        <Rule>
          <Name>level 2</Name>
                    <ogc:Filter>

            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>category_id</ogc:PropertyName>
              <ogc:Literal>80</ogc:Literal>
            </ogc:PropertyIsEqualTo>

          </ogc:Filter>
          <MinScaleDenominator>500</MinScaleDenominator>
          <MaxScaleDenominator>2199</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>name</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">TU Text Medium</CssParameter>
              <CssParameter name="font-size">20</CssParameter>
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
            <VendorOption name="graphic-margin">6</VendorOption>
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">true</VendorOption>
            <VendorOption name="repeat">1</VendorOption>

            <!--



            <VendorOption name="repeat">1</VendorOption>

            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>

      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
