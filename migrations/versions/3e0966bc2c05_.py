"""empty message

Revision ID: 3e0966bc2c05
Revises: 
Create Date: 2024-03-11 11:53:15.807597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0966bc2c05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_image', sa.LargeBinary(), nullable=True))

    with op.batch_alter_table('book_req', schema=None) as batch_op:
        batch_op.alter_column('user_name',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('book_name',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book_req', schema=None) as batch_op:
        batch_op.alter_column('book_name',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('user_name',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('cover_image')

    # ### end Alembic commands ###