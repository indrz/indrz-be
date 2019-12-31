<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
    xmlns:sld="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
    <NamedLayer>
        <Name>wing points</Name>
        <UserStyle>
            <Name>wing points</Name>
            <Title>Default polygon style</Title>
            <Abstract>A sample style that just draws out a solid gray interior with a black 1px outline</Abstract>
            <FeatureTypeStyle>
                <Name>level 1</Name>
                  <Rule>
                    <Name>level 2</Name>
                    <MinScaleDenominator>50</MinScaleDenominator>
                    <MaxScaleDenominator>2199</MaxScaleDenominator>
                    <TextSymbolizer>
                        <Label>
                            <ogc:PropertyName>name</ogc:PropertyName>
                        </Label>
                        <Font>
                            <CssParameter name="font-family">TU Text Medium</CssParameter>
                            <CssParameter name="font-size">15</CssParameter>
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
                            </Mark>

                        </Graphic>
                        <VendorOption name="graphic-resize">proportional</VendorOption>
                        <VendorOption name="graphic-margin">5</VendorOption>
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
