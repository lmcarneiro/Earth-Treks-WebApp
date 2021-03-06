"""empty message

Revision ID: 92f64409deb3
Revises: 6c013dbe120b
Create Date: 2021-04-23 12:24:12.694927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92f64409deb3'
down_revision = '6c013dbe120b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.add_column('schedules', sa.Column('test', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'test')
    op.create_table('test',
    sa.Column('col1', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('col2', sa.VARCHAR(length=50), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
