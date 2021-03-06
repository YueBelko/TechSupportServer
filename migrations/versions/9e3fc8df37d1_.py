"""empty message

Revision ID: 9e3fc8df37d1
Revises: 734e3a8a962a
Create Date: 2021-04-23 14:07:38.723994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e3fc8df37d1'
down_revision = '734e3a8a962a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'projects', 'request_status', ['status'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'projects', type_='foreignkey')
    # ### end Alembic commands ###
