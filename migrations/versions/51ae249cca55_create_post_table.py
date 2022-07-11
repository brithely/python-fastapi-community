"""create post table

Revision ID: 51ae249cca55
Revises: 
Create Date: 2022-07-11 14:32:19.454472

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '51ae249cca55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(100)),
        sa.Column("text", sa.String(1000)),
        sa.Column("user_name", sa.String(100)),
        sa.Column("password", sa.String(256)),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )

def downgrade() -> None:
    op.drop_table('post')
