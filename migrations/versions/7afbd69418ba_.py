"""empty message

Revision ID: 7afbd69418ba
Revises: 49aeafb10324
Create Date: 2018-10-07 14:41:11.121951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7afbd69418ba'
down_revision = '49aeafb10324'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('county', 'county_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('county', sa.Column('county_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
