"""empty message

Revision ID: 1e3022fe2bec
Revises: 2057866dbafd
Create Date: 2024-02-24 15:18:39.601559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1e3022fe2bec'
down_revision: Union[str, None] = '2057866dbafd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('student_course')
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Student_Course',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_course',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('course_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('student_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('test', mysql.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name='student_course_ibfk_1'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='student_course_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Student_Course')
    # ### end Alembic commands ###
