"""empty message

Revision ID: bc9a6dc7b377
Revises: 22beab22e158
Create Date: 2018-11-21 15:37:43.156933

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc9a6dc7b377'
down_revision = '22beab22e158'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'body',
               existing_type=mysql.MEDIUMTEXT(),
               type_=sa.Text(length=1000000),
               existing_nullable=True)
    op.alter_column('post', 'description',
               existing_type=mysql.TEXT(),
               type_=sa.Text(length=1000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'description',
               existing_type=sa.Text(length=1000),
               type_=mysql.TEXT(),
               existing_nullable=True)
    op.alter_column('post', 'body',
               existing_type=sa.Text(length=1000000),
               type_=mysql.MEDIUMTEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###