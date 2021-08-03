"""empty message

Revision ID: 8d671249a8f1
Revises: 208eedbe59a5
Create Date: 2021-07-30 08:05:37.068516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d671249a8f1'
down_revision = '208eedbe59a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_hash')
    # ### end Alembic commands ###