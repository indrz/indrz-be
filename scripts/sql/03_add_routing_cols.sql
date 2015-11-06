ALTER TABLE geodata.eg00_networklines ADD COLUMN source INTEGER;
ALTER TABLE geodata.eg00_networklines ADD COLUMN target INTEGER;
ALTER TABLE geodata.eg00_networklines ADD COLUMN cost DOUBLE PRECISION;
ALTER TABLE geodata.eg00_networklines ADD COLUMN length DOUBLE PRECISION;
UPDATE geodata.eg00_networklines set length = ST_Length(geom);