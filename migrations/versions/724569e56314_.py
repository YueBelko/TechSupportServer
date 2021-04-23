"""empty message

Revision ID: 724569e56314
Revises: 5ac8a290ef89
Create Date: 2021-04-23 13:48:11.716252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '724569e56314'
down_revision = '5ac8a290ef89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('remove_in_report', sa.Boolean(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_orgname', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_orgname'], ['org_name.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('changeintheproject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_project', sa.Integer(), nullable=True),
    sa.Column('id_clients', sa.Integer(), nullable=True),
    sa.Column('changes', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_clients'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['id_project'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projectinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_project', sa.Integer(), nullable=True),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['id_project'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projectrequest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_project', sa.Integer(), nullable=True),
    sa.Column('id_clients', sa.Integer(), nullable=True),
    sa.Column('id_worker_created', sa.Integer(), nullable=True),
    sa.Column('id_worker_responsible', sa.Integer(), nullable=True),
    sa.Column('id_contacts', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('remove', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_clients'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['id_contacts'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['id_project'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['id_worker_created'], ['worker.id'], ),
    sa.ForeignKeyConstraint(['id_worker_responsible'], ['worker.id'], ),
    sa.ForeignKeyConstraint(['status'], ['request_status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projectrequest')
    op.drop_table('projectinfo')
    op.drop_table('changeintheproject')
    op.drop_table('projects')
    op.drop_table('request_status')
    # ### end Alembic commands ###
