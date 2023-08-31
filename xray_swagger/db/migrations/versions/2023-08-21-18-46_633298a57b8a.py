"""Create SCHEMA

Revision ID: 633298a57b8a
Revises: 819cbf6e030b
Create Date: 2023-08-21 18:46:13.026246

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "633298a57b8a"
down_revision = "819cbf6e030b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "device",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("model_series", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("manufacturer", sa.String(length=255), nullable=False),
        sa.Column("specifications", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_device_id"), "device", ["id"], unique=False)
    op.create_table(
        "mmap_session",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("image_s3_key", sa.String(length=512), nullable=False),
        sa.Column("session_started_at", sa.DateTime(), nullable=False),
        sa.Column("session_ended_at", sa.DateTime(), nullable=True),
        sa.Column("is_preserved", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("image_s3_key"),
    )
    op.create_table(
        "settings_product_parameter",
        sa.Column("setting_param_name", sa.String(length=255), nullable=False),
        sa.Column(
            "authlevel",
            sa.Enum("OPERATOR", "SUPERVISOR", "ENGINEER", name="authlevel"),
            nullable=False,
        ),
        sa.Column("json_schema", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("setting_param_name"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("fullname", sa.String(length=64), nullable=False),
        sa.Column("phone_number", sa.String(length=128), nullable=True),
        sa.Column("company", sa.String(length=128), nullable=True),
        sa.Column("job_title", sa.String(length=128), nullable=True),
        sa.Column("joined_at", sa.DateTime(), nullable=True),
        sa.Column("last_sign_in_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "authlevel",
            sa.Enum("OPERATOR", "SUPERVISOR", "ENGINEER", name="authlevel"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("last_editor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["last_editor_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_product_id"), "product", ["id"], unique=False)
    op.create_table(
        "settings_global",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("setting_param_name", sa.String(length=255), nullable=False),
        sa.Column(
            "authlevel",
            sa.Enum("OPERATOR", "SUPERVISOR", "ENGINEER", name="authlevel"),
            nullable=False,
        ),
        sa.Column("json_schema", sa.JSON(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=True),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("last_editor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["last_editor_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inspection_session",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("image_s3_key", sa.String(length=512), nullable=False),
        sa.Column("session_started_at", sa.DateTime(), nullable=False),
        sa.Column("session_ended_at", sa.DateTime(), nullable=True),
        sa.Column("system_error", sa.Text(), nullable=True),
        sa.Column("start_mmap_session_uuid", sa.UUID(), nullable=False),
        sa.Column("start_mmap_session_ptr", sa.Integer(), nullable=False),
        sa.Column("end_mmap_session_uuid", sa.UUID(), nullable=True),
        sa.Column("end_mmap_session_ptr", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["end_mmap_session_uuid"],
            ["mmap_session.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["start_mmap_session_uuid"],
            ["mmap_session.uuid"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("image_s3_key"),
    )
    op.create_index(op.f("ix_inspection_session_id"), "inspection_session", ["id"], unique=False)
    op.create_table(
        "settings_product",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("setting_param_name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("last_editor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["last_editor_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["setting_param_name"],
            ["settings_product_parameter.setting_param_name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_product_param", "settings_product", ["product_id", "setting_param_name"], unique=True
    )
    op.create_table(
        "defect",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "defect_category",
            sa.Enum("CONTAMINANT", "METAL", "MISSING_PRODUCT", "DAMAGED", name="defectcategory"),
            nullable=False,
        ),
        sa.Column("inspection_module", sa.String(length=128), nullable=False),
        sa.Column("coordinates", sa.JSON(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("inspection_session_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["inspection_session_id"],
            ["inspection_session.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_defect_id"), "defect", ["id"], unique=False)
    op.create_table(
        "settings_product_changelog",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("settings_product_id", sa.Integer(), nullable=False),
        sa.Column("patch", sa.Text(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.Column("last_editor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["last_editor_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["settings_product_id"],
            ["settings_product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("settings_product_changelog")
    op.drop_index(op.f("ix_defect_id"), table_name="defect")
    op.drop_table("defect")
    op.drop_index("idx_product_param", table_name="settings_product")
    op.drop_table("settings_product")
    op.drop_index(op.f("ix_inspection_session_id"), table_name="inspection_session")
    op.drop_table("inspection_session")
    op.drop_table("settings_global")
    op.drop_index(op.f("ix_product_id"), table_name="product")
    op.drop_table("product")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    op.drop_table("settings_product_parameter")
    op.drop_table("mmap_session")
    op.drop_index(op.f("ix_device_id"), table_name="device")
    op.drop_table("device")
    op.execute(sa.text("DROP TYPE IF EXISTS authlevel;"))
    op.execute(sa.text("DROP TYPE IF EXISTS defectcategory;"))
    # ### end Alembic commands ###
