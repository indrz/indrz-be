from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response


class IsZoneplanAdmin(permissions.BasePermission):
    """
    Custom permission to only allow members of "zoneplan-admin" group to access.
    """

    def has_permission(self, request, view):
        # Check if the user is part of the "zoneplan-admin" group
        return request.user.groups.filter(name="zoneplan-admin").exists()

class OrganizationCodeViewSet(viewsets.ViewSet) :
    # Apply the custom permission class
    # TODO add users to the group first after deploy
    # permission_classes = [IsZoneplanAdmin]

    # Action to get the list of organization codes (without any parameter)
    def list(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT row_number() OVER (ORDER BY rd.organizationcode) AS rn,
                 rd.organizationcode,
                 org.name_de as name,
                 rd.org_color,
                 count(rd.organizationcode) as count
                FROM geodata.tu_roomdata rd
                left join geodata.tu_orgunits org on org.code = rd.organizationcode
                GROUP BY organizationcode, org.name_de, rd.org_color
                ORDER BY organizationcode
            """)
            rows = [
                {'id': row[0], 'name': row[2], 'orgcode': row[1], 'icon': 'mdi-square', 'color': row[3], 'active': False, 'count': row[4]}
                for row in cursor.fetchall()
            ]
        return Response(rows)

    # Retrieve action to get data by a specific organization code (with a parameter)
    def retrieve(self, request, pk=None, floor_num=0.0, *args, **kwargs):
        if pk is None:
            return Response({'error': 'Organization code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # get parameter floor_num from url
        floor_num = request.query_params.get('floor_num', None)
        if floor_num is None:
            return Response(
                                {'error': 'request must includde param floor_num like  api/v1/orgcode/E100/?floor_num=2.0 is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Construct FeatureCollection with the WHERE clause
        query = """
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', s.id,
                        'geometry', ST_AsGeoJSON(s.geom)::json,
                        'properties', json_build_object(
                            'id', s.id,
                            'org_id', org.org_id,
                            'orgcode', t.organizationcode,
                            'org_color', t.org_color,
                            'name', t.organizationcode || ' ' || org.name_de,
                            'mainuse', t.mainuse,
                            'room_description', s.room_description,
                            'room_code', s.room_code,
                            'surface_type_id', surface_type_id,
                            'floor_num', s.floor_num
                        )
                    )
                )
            ) FROM django.buildings_buildingfloorspace AS s
            LEFT JOIN geodata.tu_roomdata t ON t.roomcode = s.room_code
            LEFT JOIN geodata.tu_orgunits org ON org.code = t.organizationcode
            WHERE t.organizationcode = %s 
            AND s.floor_num = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk, floor_num])
            feature_collection = cursor.fetchone()[0]
            return Response(feature_collection)

class OrganizationMainUseViewSet(viewsets.ViewSet) :
    # Apply the custom permission class
    # TODO add users to the group first after deploy
    # permission_classes = [IsZoneplanAdmin]

    # Action to get the list of organization codes (without any parameter)
    def list(self, request, *args, **kwargs):
        colors = [
            {"name": "1.2 Gemeinschaftsräume", "color": "#FF5733"},
            {"name": "1.4 Warteräume", "color": "#FF5733"},
            {"name": "1.5 Speiseräume", "color": "#FF5733"},
            {"name": "2.1 Büroräume", "color": "#1F78B4"},
            {"name": "2.2 Grossraumbüros", "color": "#1F78B4"},
            {"name": "2.3 Besprechungsräume", "color": "#1F78B4"},
            {"name": "2.4 Konstruktionsräume", "color": "#1F78B4"},
            {"name": "2.6 Bedienungsräume", "color": "#1F78B4"},
            {"name": "2.7 Aufsichtsräume", "color": "#1F78B4"},
            {"name": "2.8 Bürotechnikräume", "color": "#1F78B4"},
            {"name": "3.1 Werkhallen", "color": "#3FBF7F"},
            {"name": "3.2 Werkstätten", "color": "#3FBF7F"},
            {"name": "3.3 Technologische Labors", "color": "#3FBF7F"},
            {"name": "3.4 Physikalische, physikalisch-technische, elektrotechnische Labors", "color": "#3FBF7F"},
            {"name": "3.5 Chemische, bakteriologische, morphologische Labors", "color": "#3FBF7F"},
            {"name": "3.8 Küchen", "color": "#3FBF7F"},
            {"name": "3.9 Sonderarbeitsräume", "color": "#3FBF7F"},
            {"name": "4.1 Lagerräume", "color": "#B57EDC"},
            {"name": "4.2 Archive, Sammlungsräume", "color": "#B57EDC"},
            {"name": "4.3 Kühlräume", "color": "#B57EDC"},
            {"name": "4.4 Annahme- und Ausgaberäume", "color": "#B57EDC"},
            {"name": "4.5 Verkaufsräume", "color": "#B57EDC"},
            {"name": "5.1 Unterrichtsräume mit festem Gestühl", "color": "#FFD700"},
            {"name": "5.2 Allgemeine Unterrichts- und Übungsräume ohne festes Gestühl", "color": "#FFD700"},
            {"name": "5.3 Besondere Unterrichts- und Übungsräume ohne festes Gestühl", "color": "#FFD700"},
            {"name": "5.4 Bibliotheksräume", "color": "#FFD700"},
            {"name": "5.6 Versammlungsräume", "color": "#FFD700"},
            {"name": "5.7 Bühnen-, Studioräume", "color": "#FFD700"},
            {"name": "6.1 Räume mit allgemeiner medizinischer Ausstattung", "color": "#FFB6C1"},
            {"name": "7.1 Sanitärräume", "color": "#708090"},
            {"name": "7.2 Garderoben", "color": "#708090"},
            {"name": "7.3 Abstellräume", "color": "#708090"},
            {"name": "7.4 Fahrzeugabstellflächen", "color": "#708090"},
            {"name": "7.6 Räume für zentrale Technik", "color": "#708090"},
            {"name": "7.7 Schutzräume", "color": "#708090"},
            {"name": "7.9 Sonstige Räume", "color": "#708090"},
            {"name": "8.1 Abwasseraufbereitung und -beseitigung Wasserversorgung", "color": "#D2691E"},
            {"name": "8.2 Heizung und Brauchwassererwärmung", "color": "#D2691E"},
            {"name": "8.3 Raumlufttechnische Anlagen", "color": "#D2691E"},
            {"name": "8.4 Elektrische Stromversorgung", "color": "#D2691E"},
            {"name": "8.5 Fernmeldetechnik", "color": "#D2691E"},
            {"name": "8.6 Aufzugs- und Förderanlagen", "color": "#D2691E"},
            {"name": "8.7 Gase (außer für Heizzwecke) und Flüssigkeiten", "color": "#D2691E"},
            {"name": "8.8 Schächte", "color": "#D2691E"},
            {"name": "8.9 Sonstige betriebstechnische Anlagen", "color": "#D2691E"},
            {"name": "9.1 Flure, Hallen", "color": "#e0dede"},
            {"name": "9.2 Treppen", "color": "#e0dede"},
            {"name": "9.3 Schächte für Förderanlagen", "color": "#e0dede"},
            {"name": "9.4 Fahrzeugverkehrsflächen", "color": "#e0dede"},
            {"name": "9.9 Sonstige Verkehrsflächen", "color": "#e0dede"}
        ]


        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT row_number() OVER (ORDER BY mainuse) AS id,
                 mainuse
                FROM geodata.tu_roomdata
                GROUP BY mainuse
                ORDER BY mainuse;
            """)
            type_color = None
            rows =[]
            for row in cursor.fetchall():
                for color in colors:
                    if row[1] == color['name']:
                        type_color = color['color']
                rows.append({'id': row[0],
                             'name': row[1],
                             'icon': 'mdi-square',
                             'color': f'{type_color}',
                             'active': False})
        return Response(rows)


@api_view(['GET', ])  # django view function to get mainuse by name
def fetch_mainuse(request, mainuse, floor_num=None, *args):
    """
    Get mainuse by name and floor number
    example :  /api/v1/mainuse/1.5%20Speiseräume/?floor_num=0.0
    """
    floor = request.GET.get('floor_num', None)

    query = """
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(
                json_build_object(
                    'type', 'Feature',
                    'id', s.id,
                    'geometry', ST_AsGeoJSON(s.geom)::json,
                    'properties', json_build_object(
                        'id', s.id,
                        'orgcode', t.organizationcode,
                        'color', t.org_color,
                        'name', t.mainuse,
                        'mainuse', t.mainuse,
                        'room_description', s.room_description,
                        'room_code', s.room_code,
                        'surface_type_id', surface_type_id,
                        'floor_num', s.floor_num,
                        'area', t.area_m2
                    )
                )
            )
        ) FROM django.buildings_buildingfloorspace AS s
        LEFT JOIN geodata.tu_roomdata t ON t.roomcode = s.room_code
        WHERE t.mainuse = %s
        AND s.floor_num = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [mainuse, floor])
        feature_collection = cursor.fetchone()[0]
        return Response(feature_collection)


@api_view(['GET', ])  # django view function to get mainuse by name
def mainuse_list(request, *args, **kwargs):
    colors = [
        {"name": "1.2 Gemeinschaftsräume", "color": "#FF5733"},
        {"name": "1.4 Warteräume", "color": "#FF5733"},
        {"name": "1.5 Speiseräume", "color": "#FF5733"},
        {"name": "2.1 Büroräume", "color": "#1F78B4"},
        {"name": "2.2 Grossraumbüros", "color": "#1F78B4"},
        {"name": "2.3 Besprechungsräume", "color": "#1F78B4"},
        {"name": "2.4 Konstruktionsräume", "color": "#1F78B4"},
        {"name": "2.6 Bedienungsräume", "color": "#1F78B4"},
        {"name": "2.7 Aufsichtsräume", "color": "#1F78B4"},
        {"name": "2.8 Bürotechnikräume", "color": "#1F78B4"},
        {"name": "3.1 Werkhallen", "color": "#3FBF7F"},
        {"name": "3.2 Werkstätten", "color": "#3FBF7F"},
        {"name": "3.3 Technologische Labors", "color": "#3FBF7F"},
        {"name": "3.4 Physikalische, physikalisch-technische, elektrotechnische Labors", "color": "#3FBF7F"},
        {"name": "3.5 Chemische, bakteriologische, morphologische Labors", "color": "#3FBF7F"},
        {"name": "3.8 Küchen", "color": "#3FBF7F"},
        {"name": "3.9 Sonderarbeitsräume", "color": "#3FBF7F"},
        {"name": "4.1 Lagerräume", "color": "#B57EDC"},
        {"name": "4.2 Archive, Sammlungsräume", "color": "#B57EDC"},
        {"name": "4.3 Kühlräume", "color": "#B57EDC"},
        {"name": "4.4 Annahme- und Ausgaberäume", "color": "#B57EDC"},
        {"name": "4.5 Verkaufsräume", "color": "#B57EDC"},
        {"name": "5.1 Unterrichtsräume mit festem Gestühl", "color": "#FFD700"},
        {"name": "5.2 Allgemeine Unterrichts- und Übungsräume ohne festes Gestühl", "color": "#FFD700"},
        {"name": "5.3 Besondere Unterrichts- und Übungsräume ohne festes Gestühl", "color": "#FFD700"},
        {"name": "5.4 Bibliotheksräume", "color": "#FFD700"},
        {"name": "5.6 Versammlungsräume", "color": "#FFD700"},
        {"name": "5.7 Bühnen-, Studioräume", "color": "#FFD700"},
        {"name": "6.1 Räume mit allgemeiner medizinischer Ausstattung", "color": "#FFB6C1"},
        {"name": "7.1 Sanitärräume", "color": "#708090"},
        {"name": "7.2 Garderoben", "color": "#708090"},
        {"name": "7.3 Abstellräume", "color": "#708090"},
        {"name": "7.4 Fahrzeugabstellflächen", "color": "#708090"},
        {"name": "7.6 Räume für zentrale Technik", "color": "#708090"},
        {"name": "7.7 Schutzräume", "color": "#708090"},
        {"name": "7.9 Sonstige Räume", "color": "#708090"},
        {"name": "8.1 Abwasseraufbereitung und -beseitigung Wasserversorgung", "color": "#D2691E"},
        {"name": "8.2 Heizung und Brauchwassererwärmung", "color": "#D2691E"},
        {"name": "8.3 Raumlufttechnische Anlagen", "color": "#D2691E"},
        {"name": "8.4 Elektrische Stromversorgung", "color": "#D2691E"},
        {"name": "8.5 Fernmeldetechnik", "color": "#D2691E"},
        {"name": "8.6 Aufzugs- und Förderanlagen", "color": "#D2691E"},
        {"name": "8.7 Gase (außer für Heizzwecke) und Flüssigkeiten", "color": "#D2691E"},
        {"name": "8.8 Schächte", "color": "#D2691E"},
        {"name": "8.9 Sonstige betriebstechnische Anlagen", "color": "#D2691E"},
        {"name": "9.1 Flure, Hallen", "color": "#e0dede"},
        {"name": "9.2 Treppen", "color": "#e0dede"},
        {"name": "9.3 Schächte für Förderanlagen", "color": "#e0dede"},
        {"name": "9.4 Fahrzeugverkehrsflächen", "color": "#e0dede"},
        {"name": "9.9 Sonstige Verkehrsflächen", "color": "#e0dede"}
    ]

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT row_number() OVER (ORDER BY mainuse) AS id,
             mainuse
            FROM geodata.tu_roomdata
            GROUP BY mainuse
            ORDER BY mainuse;
        """)
        type_color = None
        rows = []
        for row in cursor.fetchall():
            for color in colors:
                if row[1] == color['name']:
                    type_color = color['color']
            rows.append({'id': row[0],
                         'name': row[1],
                         'icon': 'mdi-square',
                         'color': f'{type_color}',
                         'active': False})
    return Response(rows)


from django.shortcuts import render

# Create your views here.
