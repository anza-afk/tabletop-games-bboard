"""added meet-user table

Revision ID: dec1a6d08b2e
Revises: d53241390db3
Create Date: 2022-03-27 14:21:15.621969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dec1a6d08b2e'
down_revision = 'd53241390db3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meeting_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('meeting_id', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['meeting_id'], ['game_meetings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_table('games_hg',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('link_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('number_of_players', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('age', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['links_from_hg.id'], name='games_hg_link_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='games_hg_pkey')
    )
    op.create_table('links_from_hg',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('link', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='links_from_hg_pkey'),
    sa.UniqueConstraint('link', name='links_from_hg_link_key')
    )
    op.create_table('games',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('number_of_players', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('age', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='games_pkey'),
    sa.UniqueConstraint('name', name='games_name_key')
    )
    op.drop_index(op.f('ix_meeting_users_user_id'), table_name='meeting_users')
    op.drop_index(op.f('ix_meeting_users_meeting_id'), table_name='meeting_users')
    op.drop_table('meeting_users')
    # ### end Alembic commands ###
