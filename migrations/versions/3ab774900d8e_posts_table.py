"""posts table

Revision ID: 3ab774900d8e
Revises: 7d5319a7c7f5
Create Date: 2023-03-16 12:16:49.505607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ab774900d8e'
down_revision = '7d5319a7c7f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('clubs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_clubs_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clubs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_clubs_name'))

    op.drop_table('clubs')
    # ### end Alembic commands ###
