"""create results table

Revision ID: cae0ab58cd41
Revises: a2c913a31ebe
Create Date: 2020-06-13 01:34:10.160841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Float

revision = 'cae0ab58cd41'
down_revision = 'a2c913a31ebe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('results',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.DateTime, nullable=False),
                    sa.Column('results', sa.ARRAY(Float), nullable=False),
                    sa.Column('mean', sa.Float(), nullable=False),
                    sa.Column('pacientId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['pacientId'], ['pacienti.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('results')
