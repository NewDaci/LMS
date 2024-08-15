"""empty message

Revision ID: 84a8d9752293
Revises: 1ecfbaf16ed2
Create Date: 2024-03-27 10:43:41.097568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84a8d9752293'
down_revision = '1ecfbaf16ed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('content2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content2', sa.BLOB(), nullable=True))

    # ### end Alembic commands ###