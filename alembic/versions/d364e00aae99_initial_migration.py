"""Initial migration

Revision ID: d364e00aae99
Revises: 
Create Date: 2024-05-15 20:46:52.606909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd364e00aae99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('billing_address', 'state',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('billing_address', 'zip_code',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=10),
               existing_nullable=False)
    op.alter_column('billing_address', 'address',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=10),
               existing_nullable=False)
    op.alter_column('billing_address', 'tax_number',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=10),
               nullable=False)
    op.alter_column('billing_address', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('billing_address', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('billing_address', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('user', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('user', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('user', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('billing_address', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('billing_address', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('billing_address', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('billing_address', 'tax_number',
               existing_type=sa.String(length=10),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('billing_address', 'address',
               existing_type=sa.String(length=10),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('billing_address', 'zip_code',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    op.alter_column('billing_address', 'state',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###