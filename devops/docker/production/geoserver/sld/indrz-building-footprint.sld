<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
    xmlns:sld="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
    <NamedLayer>
        <Name>polygon</Name>
        <UserStyle>
            <Name>polygon</Name>
            <Title>Default polygon style</Title>
            <Abstract>A sample style that just draws out a solid gray interior with a black 1px outline</Abstract>
            <FeatureTypeStyle>
                <Name>name</Name>
                <Rule>
                    <Name>default</Name>
                    <Title>Polygon</Title>
                    <MaxScaleDenominator>20000</MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#555555</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#555555</CssParameter>
                            <CssParameter name="stroke-width">1</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                              <Rule>
                    <Name>Building Anno</Name>
                    <MinScaleDenominator>2200</MinScaleDenominator>
                    <MaxScaleDenominator>20000</MaxScaleDenominator>
                    <TextSymbolizer>
                        <Geometry>
                            <ogc:Function name="centroid">
                                <ogc:PropertyName>geom</ogc:PropertyName>
                            </ogc:Function>
                        </Geometry>
                        <Label>
                            <ogc:PropertyName>building_name</ogc:PropertyName>
                        </Label>
                        <Font>
                            <CssParameter name="font-family">Bitstream Vera Sans</CssParameter>
                            <CssParameter name="font-size">30</CssParameter>
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
                        <VendorOption name="graphic-resize">stretch</VendorOption>
                        <VendorOption name="graphic-margin">12</VendorOption>
                        <VendorOption name="goodnessOfFit">5</VendorOption>
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
                </Rule>


            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>
