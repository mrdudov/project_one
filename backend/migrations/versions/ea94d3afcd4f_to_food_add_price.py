"""to Food add price

Revision ID: ea94d3afcd4f
Revises: 7f3511607f29
Create Date: 2024-01-21 16:47:55.302206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ea94d3afcd4f'
down_revision: Union[str, None] = '7f3511607f29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food', sa.Column('price', sa.Numeric(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('food', 'price')
    # ### end Alembic commands ###
