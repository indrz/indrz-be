FILE_DIR = 'c:/Users/mdiener/GOMOGI/AAU-indrz - Dokumente/dwg-working/'
campus_names = ["Getreidemarkt", "Gusshaus", "Arsenal", "Karlsplatz", "Freihaus", ]

def linework():
    ''' Import linework from AutoDesk Autocad'''

    line_classes = [{"groupName": "someName", "layers": ["layer1", "layer2"]}]
    line_mapping = [{"layer": "name", "space_type_id": 12, "description": "door"},
                    {"layer": "name", "space_type_id": 12, "description": "door"},
                    {"layer": "name", "space_type_id": 12, "description": "door"},
                    {"layer": "name", "space_type_id": 12, "description": "door"},
                    {"layer": "name", "space_type_id": 12, "description": "door"},
                    ]

    return False

cad_spaces_lyrs = [('0-fussboden')]
cad_spaces_names = tuple(cad_spaces_lyrs)

linefeatures = [
    {"layer": "0-wand-gk220-F90", "type": "furniture", "cadfiles": ["lakeside b01 eg"]},
    {"layer": "ar_einrichtung", "type": "ramp, walls, doors", "cadfiles": ["A1_EG"]},
    {"layer": "0-tueren", "type": "doors", "cadfiles": ["Musili_R_OG01"]},
    {"layer": "Div.Linien", "type": "doors,ramps,furniture", "cadfiles": ["B11,B10"]},

]

cad_layer_names = [x['layer'] for x in linefeatures]
cad_layer_names = tuple(cad_layer_names)

umriss_layers = [{'layer': 'Umriss', 'type': 'umriss', 'cadfiles': ['B11,B10,Mensa']}]

umriss_layer_names = [x['layer'] for x in umriss_layers]
umriss_layer_names = tuple(umriss_layer_names)

cad_construction_names = 'Poly Baustelle'

cad_label_layers = ['0-raum-bez']
cad_umriss = [('0-fussboden')]
cad_umriss_layers = tuple(cad_umriss)

building_code_map = [
{"building_code":"Z","dwg_building_code":"Z", "campus": "AAU Main"},
{"building_code":"S","dwg_building_code":"Z", "campus": "AAU Main"},
{"building_code":"O","dwg_building_code":"Z", "campus": "AAU Main"},
{"building_code":"L","dwg_building_code":"Z", "campus": "AAU Main"},
{"building_code":"B01","dwg_building_code":"B01", "campus": "Lakeside"},
{"building_code":"B02","dwg_building_code":"B02", "campus": "Lakeside"},
{"building_code":"B03","dwg_building_code":"B03", "campus": "Lakeside"},
{"building_code":"B04","dwg_building_code":"B04", "campus": "Lakeside"},
{"building_code":"B07","dwg_building_code":"B07", "campus": "Lakeside"},
{"building_code":"B08","dwg_building_code":"B08", "campus": "Lakeside"},
{"building_code":"B09","dwg_building_code":"B09", "campus": "Lakeside"},
{"building_code":"B10","dwg_building_code":"B10", "campus": "Lakeside"},
{"building_code":"B11","dwg_building_code":"B11", "campus": "Lakeside"},
{"building_code":"B13","dwg_building_code":"B13", "campus": "Lakeside"},
{"building_code":"C","dwg_building_code":"C", "campus": "Sterneckstrasse"},
{"building_code":"B13","dwg_building_code":"B13", "campus": "Lakeside"},
]


room_types = [
  {"type_code": 33, "type_name": "Aufzug"},
  {"type_code": 33, "type_name": "Lift"},
  {"type_code": 44, "type_name": "Aula"},
  {"type_code": 91, "type_name": "WC"},
  {"type_code": 91, "type_name": "Dusch"},
  {"type_code": 91, "type_name": "WC"},
  {"type_code": 6, "type_name": "Labor"},
  {"type_code": 79, "type_name": "Stiege"},
  {"type_code": 6, "type_name": "Drohnenhalle"},
  {"type_code": 6, "type_name": "Sammlung"}
]


category_types = [
  {"type_code": 94, "type_name": "Funktionsflächen"},
  {"type_code": 63, "type_name": "Büros und Sitzungsräume"},
  {"type_code": 44, "type_name": "Verkehrsflächen"},
  {"type_code": 94, "type_name": "Wohn- und Aufenthaltsräume"},
  {"type_code": 94, "type_name": "Sonstige Nutzung"},
  {"type_code": 63, "type_name": "Werkstätten und Labors"},
  {"type_code": 6, "type_name": "Unterrichtsräume und Bibliotheken"},
  {"type_code": 94, "type_name": "Lager und Archive"}]


# OLD space_types imported
#TODO remove this below
# room_types =[
# {"type_code": 94, "type_name": "Abstellräume"},
# {"type_code": 94, "type_name": "Abwasseraufbereitung und -beseitigung"},
# {"type_code": 6, "type_name": "Allg. Unterrichtsräume ohne festem Gestühl"},
# {"type_code": 94, "type_name": "Annahme- & Ausgaberäume"},
# {"type_code": 94, "type_name": "Archive, Sammlungsräume"},
# {"type_code": 94, "type_name": "Aufenthaltsräume"},
# {"type_code": 94, "type_name": "Aufsichtsräume"},
# {"type_code": 33, "type_name": "Aufzugs- & Förderanlagen"},
# {"type_code": 94, "type_name": "Bedienungsräume"},
# {"type_code": 6, "type_name": "Bes. Unterrichtsräume ohne festem Gestühl"},
# {"type_code": 63, "type_name": "Besprechungsräume"},
# {"type_code": 63, "type_name": "Bibliotheksräume"},
# {"type_code": 63, "type_name": "Büroräume"},
# {"type_code": 94, "type_name": "Bürotechnikräume"},
# {"type_code": 63, "type_name": "Computerräume für Studierende"},
# {"type_code": 63, "type_name": "Computertechnische Anlagen"},
# {"type_code": 94, "type_name": "Elektrische Versorgung"},
# {"type_code": 94, "type_name": "Fahrzeugabstellflächen"},
# {"type_code": 94, "type_name": "Fernmeldetechnik, LAN"},
# {"type_code": 44, "type_name": "Flure, Hallen"},
# {"type_code": 94, "type_name": "Garderoben"},
# {"type_code": 94, "type_name": "Gase und Flüssigkeiten"},
# {"type_code": 63, "type_name": "Gemeinschaftsräume"},
# {"type_code": 63, "type_name": "Großraumbüros"},
# {"type_code": 94, "type_name": "Heizung und Brauchwassererwärmung"},
# {"type_code": 94, "type_name": "Küchen"},
# {"type_code": 94, "type_name": "Kühlräume"},
# {"type_code": 94, "type_name": "Lagerräume"},
# {"type_code": 94, "type_name": "Nutzung (noch) unklar"},
# {"type_code": 63, "type_name": "Pausenräume"},
# {"type_code": 94, "type_name": "Raumlufttechnische Anlagen"},
# {"type_code": 91, "type_name": "Sanitärräume"},
# {"type_code": 94, "type_name": "Schächte für Förderanlagen"},
# {"type_code": 94, "type_name": "Sonderarbeitsräume"},
# {"type_code": 63, "type_name": "Sonstige Büroflächen"},
# {"type_code": 94, "type_name": "Sonstige Räume"},
# {"type_code": 94, "type_name": "Sonstige betriebstechnische Anlagen"},
# {"type_code": 94, "type_name": "Speiseräume"},
# {"type_code": 63, "type_name": "Sporträume"},
# {"type_code": 6, "type_name": "Technologische Labors"},
# {"type_code": 79, "type_name": "Treppen"},
# {"type_code": 6, "type_name": "Unterrichtsräume mit festem Gestühl"},
# {"type_code": 6, "type_name": "Unterrichtstechnische Anlageräume"},
# {"type_code": 94, "type_name": "Verkaufsräume"},
# {"type_code": 63, "type_name": "Versammlungsräume"},
# {"type_code": 63, "type_name": "Werkstätten"}
# ]

