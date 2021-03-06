"""empty message

Revision ID: 618111c4c07d
Revises: 
Create Date: 2021-04-16 17:57:34.457710

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '618111c4c07d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.add_column('schedules', sa.Column('date_look_num', sa.Integer(), nullable=True))
    op.add_column('schedules', sa.Column('time_slot_num', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'time_slot_num')
    op.drop_column('schedules', 'date_look_num')
    # ### end Alembic commands ###
