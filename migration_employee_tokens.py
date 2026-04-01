"""Adicionar tabela employee_tokens para controle individual

Revision ID: add_employee_tokens
Create Date: 2026-04-01 09:59:55
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    op.create_table('employee_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('employee_name', sa.String(length=120), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_tokens_company_id'), 'employee_tokens', ['company_id'], unique=False)
    op.create_index(op.f('ix_employee_tokens_token'), 'employee_tokens', ['token'], unique=True)
    op.create_index(op.f('ix_employee_tokens_used'), 'employee_tokens', ['used'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_employee_tokens_used'), table_name='employee_tokens')
    op.drop_index(op.f('ix_employee_tokens_token'), table_name='employee_tokens')
    op.drop_index(op.f('ix_employee_tokens_company_id'), table_name='employee_tokens')
    op.drop_table('employee_tokens')
