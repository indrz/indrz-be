<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
                       xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>All spaces</Name>
    <UserStyle>
      <Name>All spaces</Name>
      <Title>all spaces</Title>
      <Abstract>spaces</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Title>all spaces</Title>
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
          <Title>Stiegen, Lift, Rampen, Flur, Gang</Title>
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
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>44</ogc:Literal>
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
          <Title>tuerkis</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>64</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#CCCCFF</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


        <Rule>
          <Title>tuerkis</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>65</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#99FFVV</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


        <Rule>
          <Title>Hörsaal, Seminaar, zeichen</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>6</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#006BAC</CssParameter>
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
            <ogc:Or>

              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>91</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>104</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>105</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>space_type_id</ogc:PropertyName>
                <ogc:Literal>106</ogc:Literal>
              </ogc:PropertyIsEqualTo>


            </ogc:Or>
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
          <Title>Sekretariat, Rektor, Dekanat</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>103</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#41A1DA</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>

        </Rule>

        <Rule>
          <Title>Werkstätten, Büro, Besprechungsraum, Bibliothek, Labor</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>50</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#8AD1F5</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

        <Rule>
          <Title>Wall, Wall Cavity</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>89</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

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
          <Title>veranstaltungräume, Prechtsaale</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>63</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>

          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#99FFCC</CssParameter>
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
          <Title>First Aid</Title>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>109</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>


          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#42A12B</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>


        <Rule>
          <Title>Other space type</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>94</ogc:Literal>
            </ogc:PropertyIsLike>
          </ogc:Filter>
          <MaxScaleDenominator>8000</MaxScaleDenominator>


          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#555555</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#5c5c5c</CssParameter>
              <CssParameter name="stroke-width">0.26</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>

        <Rule>
          <Title>Other space type</Title>
          <ogc:Filter>
            <ogc:PropertyIsLike wildCard="%" singleChar="?" escape="|">
              <ogc:PropertyName>space_type_id</ogc:PropertyName>
              <ogc:Literal>93</ogc:Literal>
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

      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
