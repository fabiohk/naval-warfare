"""empty message

Revision ID: bd165b5ce344
Revises: 5f5670280d5a
Create Date: 2021-04-03 20:08:45.431411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd165b5ce344'
down_revision = '5f5670280d5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_game_players_id', table_name='game_players')
    op.drop_table('game_players')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_players',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], name='game_players_game_id_fkey'),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], name='game_players_player_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='game_players_pkey')
    )
    op.create_index('ix_game_players_id', 'game_players', ['id'], unique=False)
    # ### end Alembic commands ###