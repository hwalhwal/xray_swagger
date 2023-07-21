from peewee_migrate import Router

from xray_swagger.db.database import db

router = Router(db)

# Create migration
router.create("migration_name")

# Run migration/migrations
router.run("migration_name")

# Run all unapplied migrations
router.run()
