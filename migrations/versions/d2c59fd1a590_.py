"""empty message

Revision ID: d2c59fd1a590
Revises: 66668d429d11
Create Date: 2021-04-15 15:17:44.483912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2c59fd1a590'
down_revision = '66668d429d11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.Column('unp', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('u_address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('block', sa.Boolean(), nullable=True),
    sa.Column('blocking_reason', sa.Text(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.Column('orgname', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['orgname'], ['org_name.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_clients', sa.Integer(), nullable=True),
    sa.Column('data_block', sa.DateTime(), nullable=True),
    sa.Column('blocking_reason', sa.Text(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_clients'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients_pc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_clients', sa.Integer(), nullable=True),
    sa.Column('rdesk_soft', sa.String(), nullable=True),
    sa.Column('rdesk_id', sa.String(), nullable=True),
    sa.Column('remove', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_clients'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_clients', sa.Integer(), nullable=True),
    sa.Column('fio', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_clients'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    op.drop_table('clients_pc')
    op.drop_table('block_history')
    op.drop_table('clients')
    # ### end Alembic commands ###