"""create pacienti table

Revision ID: a2c913a31ebe
Revises: e8fb31514e85
Create Date: 2020-03-05 11:35:17.121618

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a2c913a31ebe'
down_revision = 'e8fb31514e85'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pacienti',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('numeParinte', sa.String(length=255), nullable=False),
                    sa.Column('prenumeParinte', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), server_default='', nullable=False),
                    sa.Column('telefon', sa.Integer(), nullable=False),
                    sa.Column('numeCopil', sa.String(length=255), nullable=False),
                    sa.Column('prenumeCopil', sa.String(length=255), nullable=False),
                    sa.Column('parola', sa.String(length=100), server_default='', nullable=False),
                    sa.Column('status', sa.String(length=100), server_default='', nullable=False),
                    sa.Column('varsta', sa.Integer(), nullable=False),
                    sa.Column('medicId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['medicId'], ['medici.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )


def downgrade():
    op.drop_table('pacienti')
