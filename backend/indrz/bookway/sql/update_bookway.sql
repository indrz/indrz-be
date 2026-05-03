UPDATE django.bookway_shelfdata SET system_from_array = regexp_split_to_array(system_from, '[-./:\s]');
UPDATE django.bookway_shelfdata SET system_to_array = regexp_split_to_array(system_to, '[-./:\s]');
