"""add place

Revision ID: 9ef751e716ee
Revises: 7d9ca487c306
Create Date: 2022-04-05 21:47:37.854211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef751e716ee'
down_revision = '7d9ca487c306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('game_meetings', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_game_meetings_city_id'), 'game_meetings', ['city_id'], unique=False)
    op.create_foreign_key(None, 'game_meetings', 'cities', ['city_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game_meetings', type_='foreignkey')
    op.drop_index(op.f('ix_game_meetings_city_id'), table_name='game_meetings')
    op.drop_column('game_meetings', 'city_id')
    op.drop_table('cities')
    op.drop_table('countries')
    # ### end Alembic commands ###
