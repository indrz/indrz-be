update django.buildings_buildingfloorspace as d set room_description = a.description from geodata.tu_roomdata as a
     where d.room_code = a.roomcode;


