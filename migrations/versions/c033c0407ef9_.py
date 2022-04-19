"""empty message

Revision ID: c033c0407ef9
Revises: 80a80b886ca9
Create Date: 2022-04-15 12:34:26.645066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c033c0407ef9'
down_revision = '80a80b886ca9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('game_meetings', 'deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('game_meetings', 'deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###