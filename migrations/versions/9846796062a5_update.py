"""update

Revision ID: 9846796062a5
Revises: 7934c3d4fe61
Create Date: 2018-11-22 20:15:15.617218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9846796062a5'
down_revision = '7934c3d4fe61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
