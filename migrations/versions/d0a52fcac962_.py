"""empty message

Revision ID: d0a52fcac962
Revises: 43aae8772f5a
Create Date: 2021-08-04 08:30:28.529281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0a52fcac962'
down_revision = '43aae8772f5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'body_html')
    # ### end Alembic commands ###
