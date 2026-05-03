CREATE OR REPLACE FUNCTION django.commonness(
  a1 TEXT [],
  a2 TEXT [])

  RETURNS INT LANGUAGE plpgsql
AS $$
DECLARE
  i      INT = 0;
  l      INT = 0;
  result INT = 0;
BEGIN

  l = array_length(a1, 1);
  IF l > array_length(a2, 1)
  THEN
    l = array_length(a2, 1);
  END IF;

  FOR i IN 1..l LOOP
    IF a1 [i] = a2 [i]
    THEN
      result = result + 1;
    ELSE
      RETURN result;
    END IF;
  END LOOP;

  RETURN result;
END;
$$;


CREATE OR REPLACE FUNCTION django.equalize_arrays(
  key          TEXT [],
  sys_array    TEXT [],
  append_value text)

  RETURNS text [] LANGUAGE plpgsql
AS $$
DECLARE
  i      INT = 0;
  l1     INT = 0;
  l2     INT = 0;
  result INT = 0;
BEGIN
  -- array leng in db must be as long as incoming array
  l1 = array_length(key, 1);
  l2 = array_length(sys_array, 1);

  IF l1 > l2
  THEN
    result = l1 - l2;

    for i in 1..result LOOP
      sys_array = array_append(sys_array, append_value);
    END LOOP;

  END IF;


  RETURN sys_array;
END;
$$;


CREATE OR REPLACE FUNCTION bookway_index_changes()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.system_from <> OLD.system_from THEN
	     UPDATE django.bookway_shelfdata SET system_from_array = regexp_split_to_array(system_from, '[-./:\s]')
	        WHERE system_from_array notnull;
	     UPDATE django.bookway_shelfdata SET system_from_jsonb = to_json(system_from_array)
	        WHERE system_from_array notnull;
	END IF;

	IF NEW.system_to <> OLD.system_to THEN
	     UPDATE django.bookway_shelfdata SET system_to_array = regexp_split_to_array(system_to, '[-./:\s]')
	        WHERE system_to_array notnull;
	     UPDATE django.bookway_shelfdata SET system_to_jsonb = to_json(system_to_array)
	        WHERE system_to_array notnull;
	END IF;

	RETURN NEW;
END;
$$


DROP TRIGGER IF EXISTS bookway_system_fromto_changes
ON django.bookway_shelfdata;

CREATE TRIGGER bookway_system_fromto_changes
  AFTER UPDATE
  ON django.bookway_shelfdata
  FOR EACH ROW
  EXECUTE PROCEDURE django.bookway_index_changes();