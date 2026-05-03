BEGIN;
--
-- Create model Building
--
CREATE TABLE "buildings_building" ("id" bigserial NOT NULL PRIMARY KEY, "street" varchar(256) NULL, "house_number" varchar(10) NULL, "postal_code" varchar(8) NULL, "municipality" varchar(256) NULL, "city" varchar(256) NULL, "country" varchar(256) NULL, "name" varchar(256) NULL, "description" text NULL, "phone" varchar(32) NULL, "email" varchar(256) NULL, "website" varchar(256) NULL, "geom" geometry(POINT,3857) NULL, "building_name" varchar(128) NULL, "building_height" numeric(10, 2) NULL, "fancy_name" varchar(256) NULL, "num_floors" integer NOT NULL, "facility_number" integer NULL, "operation_hrs" varchar(60) NULL, "native_epsg" integer NULL, "detail_description" varchar(256) NULL, "wings" varchar(800) NULL);
--
-- Create model BuildingFloor
--
CREATE TABLE "buildings_buildingfloor" ("id" bigserial NOT NULL PRIMARY KEY, "short_name" varchar(150) NULL, "long_name" varchar(150) NULL, "special_name" varchar(150) NULL, "vertical_order" integer NULL, "base_elevation" integer NULL, "floor_num" double precision NULL, "floor_name" varchar(200) NULL, "floor_height" numeric(5, 2) NULL, "geom" geometry(MULTIPOLYGON,3857) NULL, "tags" varchar(255)[][] NULL);
--
-- Create model BuildingFloorPlanLine
--
CREATE TABLE "buildings_buildingfloorplanline" ("id" bigserial NOT NULL PRIMARY KEY, "short_name" varchar(150) NULL, "long_name" varchar(150) NULL, "length" numeric(10, 2) NULL, "floor_num" double precision NULL, "floor_name" varchar(200) NULL, "geom" geometry(MULTILINESTRING,3857) NULL, "tags" varchar(150)[][] NULL);
--
-- Create model BuildingFloorSpace
--
CREATE TABLE "buildings_buildingfloorspace" ("id" bigserial NOT NULL PRIMARY KEY, "short_name" varchar(150) NULL, "long_name" varchar(150) NULL, "area" numeric(10, 2) NULL, "perimeter" numeric(10, 2) NULL, "floor_num" double precision NULL, "floor_name" varchar(200) NULL, "geom" geometry(MULTIPOLYGON,3857) NULL, "room_external_id" varchar(150) NULL, "room_number" varchar(150) NULL, "room_number_sign" varchar(150) NULL, "room_description" varchar(150) NULL, "room_code" varchar(150) NULL, "capacity" integer NULL, "tag" text NULL, "tags" varchar(150)[][] NULL);
--
-- Create model Campus
--
CREATE TABLE "buildings_campus" ("id" bigserial NOT NULL PRIMARY KEY, "campus_name" varchar(128) NULL, "description" varchar(256) NULL, "geom" geometry(MULTIPOLYGON,3857) NULL, "sort_order" integer NULL);
--
-- Create model LtAccessType
--

CREATE TABLE "buildings_ltaccesstype" ("id" bigserial NOT NULL PRIMARY KEY, "code" varchar(150) NULL, "name" varchar(256) NULL);
--
-- Create model LtCondition
--
CREATE TABLE "buildings_ltcondition" ("id" bigserial NOT NULL PRIMARY KEY, "code" varchar(150) NULL, "name" varchar(256) NULL);
--
-- Create model LtPlanLineType
--
CREATE TABLE "buildings_ltplanlinetype" ("id" bigserial NOT NULL PRIMARY KEY, "code" varchar(150) NULL, "name" varchar(256) NULL);
--
-- Create model LtSpaceType
--
CREATE TABLE "buildings_ltspacetype" ("id" bigserial NOT NULL PRIMARY KEY, "code" varchar(150) NULL, "name" varchar(256) NULL);
--
-- Create model Organization
--
CREATE TABLE "buildings_organization" ("id" bigserial NOT NULL PRIMARY KEY, "street" varchar(256) NULL, "house_number" varchar(10) NULL, "postal_code" varchar(8) NULL, "municipality" varchar(256) NULL, "city" varchar(256) NULL, "country" varchar(256) NULL, "name" varchar(256) NULL, "description" text NULL, "phone" varchar(32) NULL, "email" varchar(256) NULL, "website" varchar(256) NULL, "geom" geometry(POINT,3857) NULL, "owner" varchar(128) NULL, "legal_form" varchar(128) NULL, "num_buildings" integer NULL);
--
-- Create model Wing
--
CREATE TABLE "buildings_wing" ("id" bigserial NOT NULL PRIMARY KEY, "short_name" varchar(150) NULL, "long_name" varchar(150) NULL, "area" numeric(10, 2) NULL, "perimeter" numeric(10, 2) NULL, "floor_num" double precision NULL, "floor_name" varchar(200) NULL, "geom" geometry(MULTIPOLYGON,3857) NULL, "name" varchar(256) NULL, "abbreviation" varchar(20) NULL, "fk_access_type_id" bigint NULL, "fk_building_id" bigint NULL, "fk_building_floor_id" bigint NOT NULL);
--
-- Create model InteriorFloorSection
--
CREATE TABLE "buildings_interiorfloorsection" ("id" bigserial NOT NULL PRIMARY KEY, "short_name" varchar(150) NULL, "long_name" varchar(150) NULL, "area" numeric(10, 2) NULL, "perimeter" numeric(10, 2) NULL, "floor_num" double precision NULL, "floor_name" varchar(200) NULL, "geom" geometry(MULTIPOLYGON,3857) NULL, "organization" varchar(256) NULL, "department" varchar(256) NULL, "division" varchar(256) NULL, "tags" varchar(255)[][] NULL, "fk_access_type_id" bigint NULL, "fk_building_id" bigint NULL, "fk_building_floor_id" bigint NOT NULL);

CREATE INDEX "buildings_buildingfloor_geom_id" ON "buildings_buildingfloor" USING GIST ("geom");
CREATE INDEX "buildings_buildingfloorplanline_geom_id" ON "buildings_buildingfloorplanline" USING GIST ("geom");
CREATE INDEX "buildings_buildingfloorspace_geom_id" ON "buildings_buildingfloorspace" USING GIST ("geom");
CREATE INDEX "buildings_campus_geom_id" ON "buildings_campus" USING GIST ("geom");
ALTER TABLE "buildings_wing" ADD CONSTRAINT "buildings_wing_fk_access_type_id_d3e0c50e_fk_buildings" FOREIGN KEY ("fk_access_type_id") REFERENCES "buildings_ltaccesstype" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "buildings_wing" ADD CONSTRAINT "buildings_wing_fk_building_id_55e0c2aa_fk_buildings_building_id" FOREIGN KEY ("fk_building_id") REFERENCES "buildings_building" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "buildings_wing" ADD CONSTRAINT "buildings_wing_fk_building_floor_id_a716cc93_fk_buildings" FOREIGN KEY ("fk_building_floor_id") REFERENCES "buildings_buildingfloor" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "buildings_wing_geom_id" ON "buildings_wing" USING GIST ("geom");
CREATE INDEX "buildings_wing_fk_access_type_id_d3e0c50e" ON "buildings_wing" ("fk_access_type_id");
CREATE INDEX "buildings_wing_fk_building_id_55e0c2aa" ON "buildings_wing" ("fk_building_id");
CREATE INDEX "buildings_wing_fk_building_floor_id_a716cc93" ON "buildings_wing" ("fk_building_floor_id");
ALTER TABLE "buildings_interiorfloorsection" ADD CONSTRAINT "buildings_interiorfl_fk_access_type_id_fae97abf_fk_buildings" FOREIGN KEY ("fk_access_type_id") REFERENCES "buildings_ltaccesstype" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "buildings_interiorfloorsection" ADD CONSTRAINT "buildings_interiorfl_fk_building_id_310dc0fb_fk_buildings" FOREIGN KEY ("fk_building_id") REFERENCES "buildings_building" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "buildings_interiorfloorsection" ADD CONSTRAINT "buildings_interiorfl_fk_building_floor_id_9f80e5b9_fk_buildings" FOREIGN KEY ("fk_building_floor_id") REFERENCES "buildings_buildingfloor" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "buildings_interiorfloorsection_geom_id" ON "buildings_interiorfloorsection" USING GIST ("geom");
CREATE INDEX "buildings_interiorfloorsection_fk_access_type_id_fae97abf" ON "buildings_interiorfloorsection" ("fk_access_type_id");
CREATE INDEX "buildings_interiorfloorsection_fk_building_id_310dc0fb" ON "buildings_interiorfloorsection" ("fk_building_id");
CREATE INDEX "buildings_interiorfloorsection_fk_building_floor_id_9f80e5b9" ON "buildings_interiorfloorsection" ("fk_building_floor_id");
COMMIT;
