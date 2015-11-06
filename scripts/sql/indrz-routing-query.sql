SELECT seq, id1 AS node, id2 AS edge, ST_Length(geom) AS cost, floor,
           ST_AsGeoJSON(geom) AS geoj
      FROM pgr_dijkstra(
        'SELECT id as id, source, target, st_length(geom) as cost
         FROM geodata.networklines_3857',
        36,495, FALSE, FALSE
      ) AS dij_route
      JOIN  geodata.networklines_3857 AS input_network
      ON dij_route.id2 = input_network.id ;