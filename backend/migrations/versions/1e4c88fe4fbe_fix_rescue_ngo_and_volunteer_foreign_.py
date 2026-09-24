"""Fix rescue volunteer foreign key

Revision ID: 1e4c88fe4fbe
Revises: 6868f8f93528
"""

from alembic import op


revision = "1e4c88fe4fbe"
down_revision = "6868f8f93528"
branch_labels = None
depends_on = None


def upgrade():

    op.create_foreign_key(
        "fk_rescues_assigned_volunteer_volunteers",
        "rescues",
        "volunteers",
        ["assigned_volunteer"],
        ["id"]
    )


def downgrade():

    op.drop_constraint(
        "fk_rescues_assigned_volunteer_volunteers",
        "rescues",
        type_="foreignkey"
    )