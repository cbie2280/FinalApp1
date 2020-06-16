"""create medici table

Revision ID: e8fb31514e85
Revises: 
Create Date: 2020-03-04 16:13:35.893920

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e8fb31514e85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('medici',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nume', sa.String(length=255), nullable=False),
                    sa.Column('prenume', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), server_default='', nullable=False),
                    sa.Column('parola', sa.String(length=100), server_default='', nullable=False),
                    sa.Column('status', sa.String(length=100), server_default='', nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),

                    )


def downgrade():
    op.drop_table('medici')
