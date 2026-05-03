linefeatures = [
{'layer': 'E_S29', 'type': 'sink'},
{'layer': 'O_F49', 'type': 'window'},
{'layer': 'M_V29 (Fassadenverkleidung)', 'type': 'window'},
{'layer': 'S_29', 'type': 'stairs'},
{'layer': 'S__29', 'type': 'stairs'},
{'layer': 'S_27', 'type':'stairs'},
{'layer': 'S__27', 'type':'stairs'},
{'layer': 'X_S_29', 'type':'stairs'},
{'layer': 'E_M26', 'type':'chairs'},
{'layer': 'H_L27', 'type':'elevator'},
{'layer': 'M_A29', 'type':'outer-wall'},
{'layer': 'A_A29_VER', 'type':'outer-wall'},
{'layer': 'OUT26', 'type':'outer-wall'},
{'layer': 'M_L29', 'type':'inner-wall'},
{'layer': 'M_Z29', 'type':'inner-wall'},
{'layer': 'A2-TUER-SYM050', 'type': 'door'},
{'layer': 'O_T49', 'type': 'door'},
{'layer': 'O_T29', 'type': 'door'}]

dxf_layers = [
{"category": "label", "layer":"B_127B","type":"Fläche"},
{"category": "label", "layer":"B_127N","type":"Raumnummer"},
{"category": "label", "layer":"B_227Z","type":"Raumbezeichnung"},
{"category": "construction", "layer":"Baustelle","type":"Baustelle Fläche"},
{"category": "unkown", "layer":"DA26ST","type":"Dachkonstruktion nicht sichtbar"},
{"category": "unkown", "layer":"DA27ST","type":"Dachstühle"},
{"category": "construction", "layer":"DA29DR","type":"Dachkonstruktion"},
{"category": "furniture", "layer":"E_M26","type":"Möbel"},
{"category": "unkown", "layer":"E_X49","type":""},
{"category": "furniture", "layer":"GUT_HSMoeblierung","type":"Möblierung Hörsäle und Seminarräume"},
{"category": "label", "layer":"GUT_RAUMSTEMPEL","type":"Layer für Block Raumstempel"},
{"category": "unkown", "layer":"GUT_Stahl","type":"Stahlelemente"},
{"category": "label", "layer":"GUT_Text_HS","type":"Layer für Nummerierung der Sessel in den Hörsälen"},
{"category": "unkown", "layer":"H_L26","type":"Einbauten Vordach"},
{"category": "elevator", "layer":"H_L27","type":"Einbauten Aufzug"},
{"category": "unkown", "layer":"M_A26","type":"Deckensprünge"},
{"category": "wall", "layer":"M_A28","type":"Wand tragend Draufsicht"},
{"category": "wall", "layer":"M_A29","type":"Wand tragend"},
{"category": "wall", "layer":"M_L28","type":"Wand nicht tragend leicht Draufsicht"},
{"category": "wall", "layer":"M_L29","type":"Wand nicht tragend leicht"},
{"category": "wall", "layer":"M_V29","type":"Fassadenverkleidungen"},
{"category": "wall", "layer":"M_Z28","type":"Wand nicht tragend Draufsicht"},
{"category": "wall", "layer":"M_Z29","type":"Wand nicht tragend"},
{"category": "window", "layer":"O_F49","type":"Fenster"},
{"category": "door", "layer":"O_T49","type":"Türen"},
{"category": "parking", "layer":"Parkplatz","type":"Parkplätze in Tiefgaragen"},
{"category": "symbol", "layer":"Piktogramme","type":"Symbol Baustelle"},
{"category": "construction", "layer":"Poly Baustelle","type":"Polylinie für Baustelle"},
{"category": "stairs", "layer":"S_26","type":"Stiege - alle unsichtbar darzustellenden Bauteile"},
{"category": "stairs", "layer":"S_27","type":"Stiege - alle nicht in S_29 dargestellten Stufen, Gelaender, Handlaeufe"},
{"category": "stairs", "layer":"S_29","type":"Stiegen allgemein"},
{"category": "space", "layer":"Z_009","type":"Layer für Polylinien für Flächen"},
{"category": "floor", "layer":"Z_010","type":"Gebäudeumriss"}]

outdoor_line_layers = [{'layer': 'X_BlindenleitStein', 'type': 'other'},
                       {'layer': 'X_Hof-Details', 'type': 'other'},
                       {'layer': 'X_Lichtsäule', 'type': 'other'},
                       {'layer': 'X_Tor', 'type': 'other'},
                       {'layer': 'X_Text', 'type': 'other'}]

outdoor_ply_layers = [{'layer': 'X_Bäume', 'type': 'baum'},
                  {'layer': 'X_Grünpflanzen', 'type': 'pflanzen'},
                  {'layer': 'X_Fahrradabstellanlage', 'type': 'other'},
                  {'layer': 'X_Möbel', 'type': 'moebel'},
                  {'layer': 'X_Elektroladestelle', 'type': 'other'},
                  {'layer': 'Parkplätze', 'type': 'other'}]

cad_linestring_names = [x['layer'] for x in linefeatures]

cad_linestring_layers = tuple(cad_linestring_names)
cad_construction_layers = ('Poly Baustelle')
cad_label_layers = ('B_127N', 'B_227Z','XRNR0', 'XRNR', 'GUT_RAUMSTEMPEL')
cad_spaces_layers = ('Z_009')
cad_umriss_layers = ('B_227IDTR', 'A_A29_VER', 'O_F49', 'M_A29', 'Z_010')
cad_layers_outdoor_ply = tuple([lyr['layer'] for lyr in outdoor_ply_layers])
cad_layers_outdoor_line = tuple([lyr['layer'] for lyr in outdoor_line_layers if lyr['type']=='outdoor_line'])

