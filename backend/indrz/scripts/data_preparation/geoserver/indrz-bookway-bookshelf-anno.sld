<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
  <NamedLayer>
    <Name>Library Shelf Label</Name>
    <UserStyle>
      <Name>Library Shelf Label</Name>
      <Title>Label</Title>
      <Abstract>Library shelf style</Abstract>
      <FeatureTypeStyle>
        <Name>Shelf</Name>


        <Rule>
          <Name>Shelf Letter</Name>
          <MinScaleDenominator>250</MinScaleDenominator>
          <MaxScaleDenominator>400</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>left_label</ogc:PropertyName>
            </Label>
            <Font>
              <sld:CssParameter name="font-family">Cantarell Bold</sld:CssParameter>
              <sld:CssParameter name="font-size">10</sld:CssParameter>
              <sld:CssParameter name="font-style">normal</sld:CssParameter>
              <sld:CssParameter name="font-weight">normal</sld:CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  6
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>

            <VendorOption name="repeat">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="maxAngleDelta">90</VendorOption>
            <VendorOption name="forceLeftToRight">false</VendorOption>
            <VendorOption name="spaceAround">-10</VendorOption>




            <!--
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="spaceAround">1</VendorOption>

            <VendorOption name="repeat">1</VendorOption>
            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>

                <Rule>
          <Name>Shelf Label Left</Name>
          <MinScaleDenominator>130</MinScaleDenominator>
          <MaxScaleDenominator>250</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>left_label</ogc:PropertyName>
            </Label>
            <Font>
              <sld:CssParameter name="font-family">Cantarell Bold</sld:CssParameter>
              <sld:CssParameter name="font-size">10</sld:CssParameter>
              <sld:CssParameter name="font-style">normal</sld:CssParameter>
              <sld:CssParameter name="font-weight">normal</sld:CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  12
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>


            <!--<VendorOption name="goodnessOfFit">0.1</VendorOption>-->

            <VendorOption name="repeat">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="maxAngleDelta">90</VendorOption>
            <VendorOption name="forceLeftToRight">false</VendorOption>
            <VendorOption name="spaceAround">-10</VendorOption>



            <!--
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="spaceAround">1</VendorOption>
            <VendorOption name="repeat">1</VendorOption>
            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>



        <Rule>
          <Name>Shelf Label Left</Name>
          <MinScaleDenominator>50</MinScaleDenominator>
          <MaxScaleDenominator>130</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>left_label</ogc:PropertyName>
            </Label>
            <Font>
              <sld:CssParameter name="font-family">Cantarell Bold</sld:CssParameter>
              <sld:CssParameter name="font-size">16</sld:CssParameter>
              <sld:CssParameter name="font-style">normal</sld:CssParameter>
              <sld:CssParameter name="font-weight">normal</sld:CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  20
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>


            <VendorOption name="repeat">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="maxAngleDelta">90</VendorOption>
            <VendorOption name="forceLeftToRight">false</VendorOption>
            <VendorOption name="spaceAround">-10</VendorOption>



            <!--
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="spaceAround">1</VendorOption>
            <VendorOption name="repeat">1</VendorOption>
            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>



                <Rule>
          <Name>Shelf Label Right</Name>
          <MinScaleDenominator>130</MinScaleDenominator>
          <MaxScaleDenominator>250</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>right_label</ogc:PropertyName>
            </Label>
            <Font>
              <sld:CssParameter name="font-family">Cantarell Bold</sld:CssParameter>
              <sld:CssParameter name="font-size">12</sld:CssParameter>
              <sld:CssParameter name="font-style">normal</sld:CssParameter>
              <sld:CssParameter name="font-weight">normal</sld:CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  -12
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>


            <VendorOption name="repeat">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="maxAngleDelta">90</VendorOption>
            <VendorOption name="forceLeftToRight">false</VendorOption>
            <VendorOption name="spaceAround">-10</VendorOption>



            <!-- <VendorOption name="spaceAround">-1</VendorOption>-->

            <!--
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="spaceAround">1</VendorOption>
            <VendorOption name="repeat">100</VendorOption>
            <VendorOption name="autoWrap">10</VendorOption>
            <VendorOption name="maxDisplacement">15</VendorOption>
            <VendorOption name="group">yes</VendorOption>
            <VendorOption name="spaceAround">5</VendorOption>

            -->
          </TextSymbolizer>
        </Rule>



        <Rule>
          <Name>Shelf Label Right</Name>
          <MinScaleDenominator>50</MinScaleDenominator>
          <MaxScaleDenominator>130</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>right_label</ogc:PropertyName>
            </Label>
            <Font>
              <sld:CssParameter name="font-family">Cantarell Bold</sld:CssParameter>
              <sld:CssParameter name="font-size">18</sld:CssParameter>
              <sld:CssParameter name="font-style">normal</sld:CssParameter>
              <sld:CssParameter name="font-weight">normal</sld:CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  -20
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>


            <VendorOption name="repeat">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="maxAngleDelta">90</VendorOption>
            <VendorOption name="forceLeftToRight">false</VendorOption>
            <VendorOption name="spaceAround">-10</VendorOption>



            <!-- <VendorOption name="spaceAround">-1</VendorOption>-->

            <!--
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="spaceAround">1</VendorOption>
            <VendorOption name="repeat">100</VendorOption>
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
