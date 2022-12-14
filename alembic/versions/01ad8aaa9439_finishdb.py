"""finishdb

Revision ID: 01ad8aaa9439
Revises: 7d0a18f632c3
Create Date: 2022-09-16 23:27:53.447988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01ad8aaa9439'
down_revision = '7d0a18f632c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='posts_pkey')
    )
    # ### end Alembic commands ###
