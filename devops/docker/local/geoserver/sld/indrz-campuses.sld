<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld"
                           xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc"
                           version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>indrz-campuses</sld:Name>
    <sld:UserStyle>
      <sld:Name>indrz-campuses</sld:Name>

      <sld:Title>Default polygon style</sld:Title>
      <sld:Abstract>A sample style that just draws out a solid gray interior with a black 1px outline
      </sld:Abstract>
      <sld:FeatureTypeStyle>
        <sld:Name>name</sld:Name>
        <Rule>
          <Name>Campus Wien</Name>
          <ogc:Filter>
    
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Tulln</ogc:Literal>
              </ogc:PropertyIsEqualTo>



          </ogc:Filter>
          <MinScaleDenominator>160000</MinScaleDenominator>
          <TextSymbolizer>


            <Geometry>
              <ogc:Function name="centroid">
                <ogc:PropertyName>geom</ogc:PropertyName>
              </ogc:Function>
            </Geometry>
            <Label>
              Tulln
            </Label>

            <Font>
              <CssParameter name="font-family">DejaVu Sans</CssParameter>
              <CssParameter name="font-size">16</CssParameter>
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
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#52AE32</CssParameter>
                </Fill>
              </Mark>



            </Graphic>
            <VendorOption name="graphic-resize">stretch</VendorOption>
            <VendorOption name="graphic-margin">8</VendorOption>
            <VendorOption name="goodnessOfFit">0</VendorOption>
            <VendorOption name="conflictResolution">true</VendorOption>
            <VendorOption name="repeat">1</VendorOption>

          </TextSymbolizer>
        </Rule>

        <Rule>
          <Name>Campus Tulln</Name>
          <ogc:Filter>


              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Türkenschanze</ogc:Literal>
              </ogc:PropertyIsEqualTo>



          </ogc:Filter>
          <MinScaleDenominator>160000</MinScaleDenominator>
          <TextSymbolizer>


            <Geometry>
              <ogc:Function name="centroid">
                <ogc:PropertyName>geom</ogc:PropertyName>
              </ogc:Function>
            </Geometry>
            <Label>Türkenschanze<![CDATA[ ]]>Muthgasse
            </Label>

            <Font>
              <CssParameter name="font-family">DejaVu Sans</CssParameter>
              <CssParameter name="font-size">16</CssParameter>
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
                  <DisplacementX>1</DisplacementX>
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
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#52AE32</CssParameter>
                </Fill>
              </Mark>



            </Graphic>
            <VendorOption name="graphic-resize">stretch</VendorOption>
            <VendorOption name="graphic-margin">8</VendorOption>
            <VendorOption name="goodnessOfFit">1</VendorOption>
            <VendorOption name="conflictResolution">true</VendorOption>
            <VendorOption name="repeat">1</VendorOption>

          </TextSymbolizer>
        </Rule>


        <sld:Rule>
          <sld:Name>Campus Main Locations</sld:Name>
          <ogc:Filter>
            <ogc:Or>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Muthgasse</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Türkenschanze</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Tulln</ogc:Literal>
              </ogc:PropertyIsEqualTo>

            </ogc:Or>
          </ogc:Filter>

          <sld:MinScaleDenominator>6000.0</sld:MinScaleDenominator>
          <sld:MaxScaleDenominator>160000.0</sld:MaxScaleDenominator>

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
              <sld:CssParameter name="font-size">16</sld:CssParameter>
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
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Fill>

            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>

                  <CssParameter name="fill">#52AE32</CssParameter>
                  <CssParameter name="stroke">#FFFFFF</CssParameter>
                  <CssParameter name="stroke-width">1</CssParameter>
                </Fill>

              </Mark>

            </Graphic>
            <VendorOption name="graphic-resize">proportional</VendorOption>
            <VendorOption name="graphic-margin">12</VendorOption>
            <VendorOption name="goodnessOfFit">5</VendorOption>
            <VendorOption name="conflictResolution">false</VendorOption>


          </sld:TextSymbolizer>


        </sld:Rule>


        <sld:Rule>
          <sld:Name>Campus Aussenstelle</sld:Name>
          <ogc:Filter>
            <ogc:Or>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Karlsplatz</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Getreidemarkt</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Freihaus</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Atiom Institute</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>name</ogc:PropertyName>
                <ogc:Literal>Science Center</ogc:Literal>
              </ogc:PropertyIsEqualTo>
            </ogc:Or>
          </ogc:Filter>



          <sld:MinScaleDenominator>6000.0</sld:MinScaleDenominator>
          <sld:MaxScaleDenominator>60000.0</sld:MaxScaleDenominator>

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
              <sld:CssParameter name="font-family">Arial</sld:CssParameter>
              <sld:CssParameter name="font-size">13</sld:CssParameter>
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
              <sld:CssParameter name="fill">#ffffff</sld:CssParameter>
            </sld:Fill>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">#93c383</sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <Size>80</Size>
            </sld:Graphic>

            <sld:VendorOption name="graphic-margin">1</sld:VendorOption>


          </sld:TextSymbolizer>


        </sld:Rule>



      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>