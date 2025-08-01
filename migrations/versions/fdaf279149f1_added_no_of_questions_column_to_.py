"""Added no of questions column to question  model

Revision ID: fdaf279149f1
Revises: b5ac261d5338
Create Date: 2025-03-28 23:23:17.024195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdaf279149f1'
down_revision = 'b5ac261d5338'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('no_of_questions', sa.Integer(), nullable=False))

    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.TEXT(), nullable=True))

    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('no_of_questions')

    # ### end Alembic commands ###
