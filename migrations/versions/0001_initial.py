"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-12
"""
import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("username", sa.String(80), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("preferred_language", sa.String(8), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("last_login_at", sa.DateTime()), sa.Column("is_active", sa.Boolean(), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_table("interviews", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("profession", sa.String(60), nullable=False), sa.Column("level", sa.String(30), nullable=False), sa.Column("interview_type", sa.String(40), nullable=False), sa.Column("language", sa.String(8), nullable=False), sa.Column("selected_technologies", sa.JSON(), nullable=False), sa.Column("requested_question_count", sa.Integer(), nullable=False), sa.Column("current_question_index", sa.Integer(), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("total_score", sa.Float(), nullable=False), sa.Column("started_at", sa.DateTime(), nullable=False), sa.Column("completed_at", sa.DateTime()), sa.Column("duration_seconds", sa.Integer(), nullable=False))
    op.create_index("ix_interviews_user_id", "interviews", ["user_id"])
    op.create_table("interview_questions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("interview_id", sa.Integer(), sa.ForeignKey("interviews.id"), nullable=False), sa.Column("local_question_id", sa.String(120), nullable=False), sa.Column("category", sa.String(80), nullable=False), sa.Column("question_text", sa.Text(), nullable=False), sa.Column("expected_points", sa.JSON(), nullable=False), sa.Column("keywords", sa.JSON(), nullable=False), sa.Column("order_number", sa.Integer(), nullable=False), sa.Column("is_follow_up", sa.Boolean(), nullable=False), sa.Column("parent_question_id", sa.Integer(), sa.ForeignKey("interview_questions.id")), sa.Column("shown_at", sa.DateTime(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_interview_questions_interview_id", "interview_questions", ["interview_id"])
    op.create_table("answers", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("interview_question_id", sa.Integer(), sa.ForeignKey("interview_questions.id"), nullable=False), sa.Column("answer_text", sa.Text(), nullable=False), sa.Column("score", sa.Float(), nullable=False), sa.Column("feedback", sa.Text(), nullable=False), sa.Column("strengths", sa.JSON(), nullable=False), sa.Column("weaknesses", sa.JSON(), nullable=False), sa.Column("missed_points", sa.JSON(), nullable=False), sa.Column("evaluation_source", sa.String(40), nullable=False), sa.Column("response_time_seconds", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_answers_interview_question_id", "answers", ["interview_question_id"])
    op.create_table("final_reports", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("interview_id", sa.Integer(), sa.ForeignKey("interviews.id"), nullable=False), sa.Column("overall_score", sa.Float(), nullable=False), sa.Column("technical_score", sa.Float(), nullable=False), sa.Column("communication_score", sa.Float(), nullable=False), sa.Column("strong_categories", sa.JSON(), nullable=False), sa.Column("weak_categories", sa.JSON(), nullable=False), sa.Column("recommendations", sa.JSON(), nullable=False), sa.Column("study_plan", sa.JSON(), nullable=False), sa.Column("summary", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_final_reports_interview_id", "final_reports", ["interview_id"], unique=True)
    op.create_table("user_settings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("selected_ai_provider", sa.String(40), nullable=False), sa.Column("encrypted_api_key", sa.String(800)), sa.Column("preferred_model", sa.String(120)), sa.Column("use_own_api_key", sa.Boolean(), nullable=False), sa.Column("theme", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_index("ix_user_settings_user_id", "user_settings", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_table("user_settings")
    op.drop_table("final_reports")
    op.drop_table("answers")
    op.drop_table("interview_questions")
    op.drop_table("interviews")
    op.drop_table("users")

