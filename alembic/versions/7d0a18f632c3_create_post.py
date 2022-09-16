"""create post

Revision ID: 7d0a18f632c3
Revises: e3ede6298606
Create Date: 2022-09-16 23:21:52.605245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d0a18f632c3'
down_revision = 'e3ede6298606'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, primary_key=True, nullable=False), sa.Column(
        'title', sa.String, nullable=False), sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
