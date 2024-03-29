"""empty message

Revision ID: 7eca0bbdd7b7
Revises: 3309977f4197
Create Date: 2024-03-05 23:20:10.971857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7eca0bbdd7b7'
down_revision: Union[str, None] = '3309977f4197'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('test', mysql.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###
