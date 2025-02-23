<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>indrz WING poly</Name>
    <UserStyle>
      <Title>Wing Poly</Title>
      <Abstract>wing poly style</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Title>Wing Poly</Title>

          <MinScaleDenominator>1800</MinScaleDenominator>
          <MaxScaleDenominator>2799</MaxScaleDenominator>
          <!--
          <PolygonSymbolizer>
            <Stroke>
              <CssParameter name="stroke">#0000ff</CssParameter>
              <CssParameter name="stroke-width">4</CssParameter>
              <CssParameter name="stroke-opacity">0.2</CssParameter>
            </Stroke>
          </PolygonSymbolizer>

-->
          <TextSymbolizer>
            <Geometry>
              <ogc:Function name="centroid">
                <ogc:PropertyName>geom</ogc:PropertyName>
              </ogc:Function>
            </Geometry>
            <Label>
              <ogc:PropertyName>abbreviation</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">Bitstream Vera Sans</CssParameter>
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


        <Rule>
          <Name>level 2</Name>

          <MinScaleDenominator>500</MinScaleDenominator>
          <MaxScaleDenominator>2199</MaxScaleDenominator>
          <TextSymbolizer>
            <Geometry>
              <ogc:Function name="centroid">
                <ogc:PropertyName>geom</ogc:PropertyName>
              </ogc:Function>
            </Geometry>
            <Label>
              <ogc:PropertyName>abbreviation</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">Bitstream Vera Sans</CssParameter>
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



        <VendorOption name="ruleEvaluation">first</VendorOption>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>