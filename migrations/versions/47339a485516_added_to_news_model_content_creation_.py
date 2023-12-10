"""Added to news model content, creation_date and views fields

Revision ID: 47339a485516
Revises: bc1fce99192d
Create Date: 2023-12-10 21:27:27.206533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47339a485516'
down_revision = 'bc1fce99192d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('views', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_column('views')
        batch_op.drop_column('creation_date')
        batch_op.drop_column('content')

    # ### end Alembic commands ###
