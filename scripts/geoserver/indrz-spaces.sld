<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
                       xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>All spaces</Name>
    <UserStyle>
      <Name>All spaces</Name>
      <Title>all spaces</Title>
      <Abstract>spaces</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Title>Alle Räume</Title>
          <MaxScaleDenominator>8000</MaxScaleDenominator>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#dfe8f7</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#555555</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

        <Rule>
          <Title>Stiegen, Lift, Rampen</Title>
          <ogc:Filter>
            <ogc:Or>

              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>79</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>33</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>108</ogc:Literal>
              </ogc:PropertyIsEqualTo>


            </ogc:Or>
          </ogc:Filter>


          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#FFF8CF</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

                  <Rule>
          <Title>Flure, Halle, Gang</Title>
          <ogc:Filter>
            <ogc:Or>

              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>44</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>108</ogc:Literal>
              </ogc:PropertyIsEqualTo>


            </ogc:Or>
          </ogc:Filter>

          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


                  <Rule>
          <Title>Aula</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>4</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#FFF8CF</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>




        <Rule>
          <Title>WC</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>91</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#9D9D9D</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>






        <Rule>
          <Title>Office Administration Sektretariat</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>103</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4DC7FF</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>

        </Rule>

        <Rule>
          <Title>Studentenzone EDV</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>20</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#F5D0A8</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>





          <Rule>
          <Title>Auditorium Unterrichtsräume</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>6</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#006699</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

                  <Rule>
          <Title>Versammlungsräume</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>22</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#CD81A8</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


        <Rule>
          <Title>Andere</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>94</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>


          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#dfe8f7</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
