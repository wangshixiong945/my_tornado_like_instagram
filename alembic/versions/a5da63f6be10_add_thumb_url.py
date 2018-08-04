"""add thumb_url

Revision ID: a5da63f6be10
Revises: 8de1e5a0a0c5
Create Date: 2018-08-03 23:11:51.425792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5da63f6be10'
down_revision = '8de1e5a0a0c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('thumb_url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'thumb_url')
    # ### end Alembic commands ###
