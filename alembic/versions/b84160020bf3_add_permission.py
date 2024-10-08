"""add-permission

Revision ID: b84160020bf3
Revises: 498e7422a676
Create Date: 2024-08-21 16:10:01.283904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b84160020bf3'
down_revision: Union[str, None] = '498e7422a676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission_group',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('permissions', sa.ARRAY(sa.String(length=255)), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_permission_group',
    sa.Column('classic_user_id', sa.BigInteger(), nullable=False),
    sa.Column('permission_group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['classic_user_id'], ['classic_identify.id'], ),
    sa.ForeignKeyConstraint(['permission_group_id'], ['permission_group.id'], ),
    sa.PrimaryKeyConstraint('classic_user_id', 'permission_group_id')
    )
    op.add_column('classic_identify', sa.Column('permissions', sa.ARRAY(sa.String()), server_default='{}', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('classic_identify', 'permissions')
    op.drop_table('user_permission_group')
    op.drop_table('permission_group')
    # ### end Alembic commands ###
