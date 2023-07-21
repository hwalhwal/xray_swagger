from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "dummymodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL
);
COMMENT ON TABLE "dummymodel" IS 'Model for demo purpose.';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(200) NOT NULL UNIQUE,
    "firstname" VARCHAR(128) NOT NULL,
    "lastname" VARCHAR(128) NOT NULL,
    "password" VARCHAR(128) NOT NULL,
    "phone_number" VARCHAR(128) NOT NULL,
    "job_title" VARCHAR(128) NOT NULL,
    "date_joined" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_signin" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ NOT NULL,
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "device_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "product_name" VARCHAR(255) NOT NULL,
    "product_code" VARCHAR(255) NOT NULL,
    "model_series" VARCHAR(255) NOT NULL,
    "manufacturer" VARCHAR(255) NOT NULL,
    "specifications" JSONB NOT NULL
);
COMMENT ON TABLE "device_info" IS 'Device Information.';
CREATE TABLE IF NOT EXISTS "mmap_session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "s3_key" VARCHAR(255) NOT NULL UNIQUE,
    "session_started_at" TIMESTAMPTZ NOT NULL,
    "session_ended_at" TIMESTAMPTZ NOT NULL,
    "preservation" BOOL NOT NULL
);
CREATE TABLE IF NOT EXISTS "product" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "conveyor" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial_number" VARCHAR(255) NOT NULL UNIQUE,
    "settings" JSONB NOT NULL,
    "device_info_id" INT NOT NULL REFERENCES "device_info" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "metal_detector" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial_number" VARCHAR(255) NOT NULL UNIQUE,
    "settings" JSONB NOT NULL,
    "device_info_id" INT NOT NULL REFERENCES "device_info" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rejector" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial_number" VARCHAR(255) NOT NULL UNIQUE,
    "settings" JSONB NOT NULL,
    "device_info_id" INT NOT NULL REFERENCES "device_info" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "xray_detector" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial_number" VARCHAR(255) NOT NULL UNIQUE,
    "settings" JSONB NOT NULL,
    "device_info_id" INT NOT NULL REFERENCES "device_info" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "xray_emitter" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "serial_number" VARCHAR(255) NOT NULL UNIQUE,
    "settings" JSONB NOT NULL,
    "max_scan_range" INT NOT NULL,
    "max_scan_velocity" INT NOT NULL,
    "max_voltage" DECIMAL(10,4) NOT NULL,
    "max_current" DECIMAL(10,4) NOT NULL,
    "device_info_id" INT NOT NULL REFERENCES "device_info" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "xray_emitter"."max_scan_range" IS 'in mm';
COMMENT ON COLUMN "xray_emitter"."max_scan_velocity" IS 'in cm/min';
COMMENT ON COLUMN "xray_emitter"."max_voltage" IS 'in kV';
COMMENT ON COLUMN "xray_emitter"."max_current" IS 'in mA';
COMMENT ON TABLE "xray_emitter" IS 'Hello';
CREATE TABLE IF NOT EXISTS "inspection_algorithm_rule_set" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255),
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "inspection_settings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mode" VARCHAR(255) NOT NULL,
    "ng_behavior" VARCHAR(255) NOT NULL,
    "ng_image_store_policy" VARCHAR(255) NOT NULL,
    "image_trim" VARCHAR(255),
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "product_inspection_session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "image_s3_key" VARCHAR(255) NOT NULL UNIQUE,
    "session_started_at" TIMESTAMPTZ NOT NULL,
    "session_ended_at" TIMESTAMPTZ NOT NULL,
    "start_mmap_session_ptr" INT NOT NULL,
    "end_mmap_session_ptr" INT NOT NULL,
    "system_error" TEXT,
    "end_mmap_session_id" INT NOT NULL REFERENCES "mmap_session" ("id") ON DELETE CASCADE,
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "start_mmap_session_id" INT NOT NULL REFERENCES "mmap_session" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "contaminant" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "category" SMALLINT NOT NULL,
    "shape" SMALLINT NOT NULL,
    "coordinates" JSONB NOT NULL,
    "product_inspection_session_id" INT NOT NULL REFERENCES "product_inspection_session" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "contaminant"."category" IS '이물의 카테고리를 지정한다';
COMMENT ON COLUMN "contaminant"."shape" IS '이물 표시 영역의 모양';
CREATE TABLE IF NOT EXISTS "inspection_algorithm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(7) NOT NULL,
    "schema" JSONB NOT NULL
);
COMMENT ON COLUMN "inspection_algorithm"."name" IS 'ALAT_HP: AlatHP\nAL_003E: Al003e\nAL_DONG1: Aldong1\nAL_007P2: Al007p2\nAL_009: Al009';
CREATE TABLE IF NOT EXISTS "inspection_algorithm_instance" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "parameters" JSONB NOT NULL,
    "algorithm_id" INT NOT NULL REFERENCES "inspection_algorithm" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rule_set_usage" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "order" SMALLINT NOT NULL,
    "inspection_algorithm_instance_id" INT NOT NULL REFERENCES "inspection_algorithm_instance" ("id") ON DELETE RESTRICT,
    "inspection_algorithm_ruleset_id" INT NOT NULL REFERENCES "inspection_algorithm_rule_set" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
