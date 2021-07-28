"""empty message

Revision ID: 8ad2e88b0804
Revises: d44a4f6543f9
Create Date: 2021-07-27 16:13:09.830387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ad2e88b0804'
down_revision = 'd44a4f6543f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('role', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_role_default'), 'role', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_role_default'), table_name='role')
    op.drop_column('role', 'permissions')
    op.drop_column('role', 'default')
    # ### end Alembic commands ###
