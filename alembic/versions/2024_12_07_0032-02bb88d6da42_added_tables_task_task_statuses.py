"""Added tables task, task_statuses

Revision ID: 02bb88d6da42
Revises: 
Create Date: 2024-12-07 00:32:48.539856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02bb88d6da42"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task_statuses",
        sa.Column("title", sa.String(length=32), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_statuses")),
    )
    op.create_table(
        "tasks",
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("exec_time", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["task_statuses.id"],
            name=op.f("fk_tasks_status_id_task_statuses"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )
    op.execute("INSERT INTO task_statuses (title) VALUES ('In Queue'), ('Completed')")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tasks")
    op.drop_table("task_statuses")
    # ### end Alembic commands ###
