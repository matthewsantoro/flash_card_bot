"""change set to deck

Revision ID: 6d6c8ee411fa
Revises: 320094dd591c
Create Date: 2025-01-16 18:47:04.281470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6d6c8ee411fa'
down_revision: Union[str, None] = '320094dd591c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('decks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('private', sa.BOOLEAN(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('cards_set_id_fkey', 'cards', type_='foreignkey')
    op.drop_table('sets')
    op.add_column('cards', sa.Column('deck_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'cards', 'decks', ['deck_id'], ['id'])
    op.drop_column('cards', 'set_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('set_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'cards', type_='foreignkey')
    op.create_foreign_key('cards_set_id_fkey', 'cards', 'sets', ['set_id'], ['id'])
    op.drop_column('cards', 'deck_id')
    op.create_table('sets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('private', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('creator_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name='sets_creator_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sets_pkey')
    )
    op.drop_table('decks')
    # ### end Alembic commands ###
