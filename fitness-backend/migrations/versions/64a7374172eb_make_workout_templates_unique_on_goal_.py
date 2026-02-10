from alembic import op

# revision identifiers, used by Alembic.
revision = "64a7374172eb"
down_revision = "faa5e2e590a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the old unique constraint on (goal, day_type)
    op.drop_constraint(
        "uq_workout_goal_day",           # old name used in your models.py
        "workout_templates",
        type_="unique",
    )
    # Create the new unique constraint on (goal, day_type, difficulty)
    op.create_unique_constraint(
        "uq_workout_goal_day",
        "workout_templates",
        ["goal", "day_type", "difficulty"],
    )


def downgrade() -> None:
    # Revert to the old uniqueness definition if needed
    op.drop_constraint(
        "uq_workout_goal_day",
        "workout_templates",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_workout_goal_day",
        "workout_templates",
        ["goal", "day_type"],
    )
