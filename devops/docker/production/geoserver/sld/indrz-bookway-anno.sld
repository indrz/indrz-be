<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
  <NamedLayer>
    <Name>indrz-bookway-anno</Name>
    <UserStyle>
      <Name>Library Shelf RVK Label</Name>
      <Title>RVK Label</Title>
      <Abstract>Library shelf style</Abstract>
      <FeatureTypeStyle>
        <Name>Shelf</Name>
   
        <!--    
        <Rule>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="stroke">#0000FF</CssParameter>
              <CssParameter name="stroke-width">2</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        -->

        
                <Rule>
          <Name>Shelf Letter</Name>
          <MinScaleDenominator>200</MinScaleDenominator>
          <MaxScaleDenominator>400</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>left_label</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">DejaVu Sans</CssParameter>
              <CssParameter name="font-size">11</CssParameter>
              <CssParameter name="font-color">#AAF200</CssParameter>
              <CssParameter name="font-weight">bold</CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  7
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>
            
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#3399FF</CssParameter>
                </Fill>
              </Mark>
              
            </Graphic>
            <VendorOption name="graphic-resize">stretch</VendorOption>
            <VendorOption name="graphic-margin">1</VendorOption>


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
          <MinScaleDenominator>50</MinScaleDenominator>
          <MaxScaleDenominator>200</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>right_label</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">DejaVu Sans</CssParameter>
              <CssParameter name="font-size">14</CssParameter>
              <CssParameter name="font-color">#AAF200</CssParameter>
              <CssParameter name="font-weight">bold</CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  14
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>
            
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#3399FF</CssParameter>
                </Fill>
              </Mark>
              
            </Graphic>
            <VendorOption name="graphic-resize">stretch</VendorOption>
            <VendorOption name="graphic-margin">1</VendorOption>
            <VendorOption name="goodnessOfFit">0.1</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>


  
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
          <MaxScaleDenominator>200</MaxScaleDenominator>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>left_label</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">DejaVu Sans</CssParameter>
              <CssParameter name="font-size">14</CssParameter>
              <CssParameter name="font-color">#AAF200</CssParameter>
              <CssParameter name="font-weight">bold</CssParameter>
            </Font>
            <LabelPlacement>
              <LinePlacement>
                <PerpendicularOffset>
                  -14
                </PerpendicularOffset>
              </LinePlacement>
            </LabelPlacement>
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>
            
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#3399FF</CssParameter>
                </Fill>
              </Mark>
              
            </Graphic>
            <VendorOption name="graphic-resize">stretch</VendorOption>
            <VendorOption name="graphic-margin">1</VendorOption>
            <VendorOption name="goodnessOfFit">0.1</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>
            <VendorOption name="repeat">0</VendorOption>

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