# API
TU Wien Root URL soll  
`https://api.tuwien.at/v1/indrz/`

| HTTP Methode | Endpoint| Beschreibung |
| ------ | ------ |------ |
|GET | /indrz/search/staff/?name=<string>`| Liefert alle Personen |
|GET | /indrz/search/ou/?name=<string>| Liefert alle Organisationseinheiten |
|GET | /indrz/search/rooms | Liefert alle gültigen Räume |
|GET | /indrz/search/rooms/<id> | Suche eines Raumes per Datenbank-ID |
|GET | /indrz/search/rooms?roomnumber=<string> | Suche eines Raumes per Raumnummer (topographische Bezeichnung)|
|GET | /indrz/search/rooms?description=<string> | Suche aller Räume mit Bezeichnung in getSchild(), getBezeichnung(), getRaumNr(), getZusatzbezeichnung() |
|GET | /indrz/search/rooms?ou=<string> | Suche aller Räume einer Organisationseinheit |




## Campus Organisation Search API
Liefert alle Organisationseinheiten mit <string> in getName(), getNameKurz(), getNameEngl(), getNameKurzEngl().


    `GET https://api.tuwien.at/v1/indrz/search/ou?name=<string>`


RESPONSE


```json
[
{
"name": "Universitätsrat",
"prefix": null,
"email": null,
"code": "UNIRAT",
"strasse": null,
"plz": null,
"ort": null,
"beschreibung": "Beschreibung der Orgeinheit (<b>HTML</b>)",
"gueltig_bis": null,
"gueltig_ab": "2001-01-01T00:00:00.000+0100",
"sortierung": 1,
"name_kurz": "Universitätsrat",
"code_groups": "l_universitaetsrat",
"org_key": 123,
"bezeichnung": " Universitätsrat",
"access_token": "ABCDefasdkfjljj123213",
"aktiv": true,
"kennung": "123",
"telefonnummer": null,
"kostenstelle": null,
"name_engl": null,
"uegeord_orgkey": 1,
"sonstige_telefonnummer": null,
"homepage": null,
"land": null,
"gueltig": true,
"name_kurz21": "Universitätsrat",
"name_kurz_engl": null,
"name_genitiv": "des Universitätsrates",
"name_genitiv_engl": null,
"prefix_engl": null,
"prefix_genitiv": null,
"prefix_genitiv_engl": null,
"postfix": null,
"postfix_engl": null,
"postfix_genitiv": null,
"postfix_genitiv_engl": null,
"sortierung_hierarchie": null,
"faxnummer": null,
"bezeichnung_genitiv": " des Universitätsrates",
"config_params": null,
"anzeige_gehaltszettel": false,
"eurlaub": true,
"qualitaetskriterien_url": null,
"qualitaetskriterien_url_intern": null,
"orgeh": null
}, ....
]
```


## API Search Staff
Liefert alle Personen mit <string> in getVorname(), getNachname() oder getGeburtsName(). Der Parameter name kann auch Leerzeichen enthalten. So sucht "Max Musterm" nach Kombinationen mit Max und Musterm.

    `GET https://api.tuwien.at/v1/indrz/search/staff?name=<string>`


# API Search Rooms
Gültige Räume: getBeginnDatum() <= heute <= getEndeDatum()


## Alle gültigen Räume
GET https://api.tuwien.at/v1/indrz/search/rooms

```json
[
{'buildingname': 'EA',
'buildingcolor': '#022E5F',
'capacity': 60,
'category_de': u'Hörsaal',
'category_en': 'Auditorium',
'fancyname_de': '',
'fancyname_en': '',
'floorname': 'OG06',
'pk_big': '002_00_OG06_014000',
'roomcode': 'EA.6.026',
'roomname_de': 'EA.6.026',
'roomname_en': 'EA.6.026',
'tid': 5336
}, ...
]
```

## Raum per ID

GET https://api.tuwien.at/v1/indrz/search/rooms/<id>


```json
{
'buildingname': 'EA',
'buildingcolor': '#022E5F',
'capacity': 60,
'category_de': u'Hörsaal',
'category_en': 'Auditorium',
'fancyname_de': '',
'fancyname_en': '',
'floorname': 'OG06',
'pk_big': '002_00_OG06_014000',
'roomcode': 'EA.6.026',
'roomname_de': 'EA.6.026',
'roomname_en': 'EA.6.026',
'tid': 5336
}
```

## Raum per Raumnummer

GET https://api.tuwien.at/v1/indrz/search/rooms?roomnumber=<string>

```json
{
'buildingname': 'EA',
'buildingcolor': '#022E5F',
'capacity': 60,
'category_de': u'Hörsaal',
'category_en': 'Auditorium',
'fancyname_de': '',
'fancyname_en': '',
'floorname': 'OG06',
'pk_big': '002_00_OG06_014000',
'roomcode': 'EA.6.026',
'roomname_de': 'EA.6.026',
'roomname_en': 'EA.6.026',
'tid': 5336
}
```

## Raum per Bezeichnung
Liefert alle Räume mit in <string> in getSchild(), getBezeichnung(), getRaumNr(), getZusatzbezeichnung()


GET https://api.tuwien.at/v1/indrz/search/rooms?description=<string> 

RESPONSE

```json
[
{'gebaeudename': 'EA',
'capacity': 60,
'category_de': u'Hörsaal',
'category_en': 'Auditorium',
'fancyname_de': '',
'fancyname_en': '',
'floorname': 'OG06',
'raumkey': 12345,
'roomcode': 'EA.6.026',
'roomname_de': 'EA.6.026',
'roomname_en': 'EA.6.026'
},
...
]
```

## Räume einer Organisationseinheit

GET https://api.tuwien.at/v1/indrz/search/rooms?ou=<string>


RESPONSE  json

```json
[
{'gebaeudename': 'EA',
'capacity': 60,
'category_de': u'Hörsaal',
'category_en': 'Auditorium',
'fancyname_de': '',
'fancyname_en': '',
'floorname': 'OG06',
'raumkey': 12345,
'roomcode': 'EA.6.026',
'roomname_de': 'EA.6.026',
'roomname_en': 'EA.6.026'
},
...
]
```
