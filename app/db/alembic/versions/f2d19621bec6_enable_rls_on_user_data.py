"""Enable RLS on user data

Revision ID: f2d19621bec6
Revises: eec26c6acadb
Create Date: 2024-12-17 15:17:10.092801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2d19621bec6'
down_revision: Union[str, None] = 'eec26c6acadb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY user_data_ac_owner_full_access ON user_data
    FOR ALL
    USING (
        (current_setting('auth.actor_id') = user_data.user_id::text)
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP POLICY IF EXISTS user_data_ac_owner_full_access ON user_data;
    
    ALTER TABLE user_data DISABLE ROW LEVEL SECURITY;
    """)
