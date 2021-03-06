"""empty message

Revision ID: 821c0aa47711
Revises: 4e5079d3bc6f
Create Date: 2017-03-01 19:59:45.636203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '821c0aa47711'
down_revision = '4e5079d3bc6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
