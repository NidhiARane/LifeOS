"""
AI Model - ChatMessage Model
Stores conversation history for user interactions with AI
"""
from datetime import datetime
from app import db

class ChatMessage(db.Model):
    """
    Chat Message Model
    Stores messages from both user and AI assistant
    """
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Message Content
    message_type = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)

    # Metadata
    topic = db.Column(db.String(100))  # finance, health, habits, general

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship - backref creates user attribute on ChatMessage, chat_messages on User
    user = db.relationship('User', backref=db.backref('chat_messages', cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return f'<ChatMessage {self.message_type} - {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'message_type': self.message_type,
            'content': self.content,
            'topic': self.topic,
            'created_at': self.created_at.isoformat()
        }


class AIReport(db.Model):
    """
    AI Report Model
    Stores weekly AI-generated reports and insights
    """
    __tablename__ = 'ai_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Report Content
    report_type = db.Column(db.String(50), nullable=False)  # 'weekly', 'monthly'
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Report Data
    financial_summary = db.Column(db.Text)  # JSON or text summary
    health_summary = db.Column(db.Text)     # JSON or text summary
    habits_summary = db.Column(db.Text)     # JSON or text summary

    # Insights
    key_insights = db.Column(db.Text)
    recommendations = db.Column(db.Text)

    # Metadata
    report_date = db.Column(db.DateTime, nullable=False)
    week_start = db.Column(db.DateTime)
    week_end = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship - backref creates user attribute on AIReport, ai_reports on User
    user = db.relationship('User', backref=db.backref('ai_reports', cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return f'<AIReport {self.title} - {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'report_type': self.report_type,
            'title': self.title,
            'content': self.content,
            'key_insights': self.key_insights,
            'recommendations': self.recommendations,
            'report_date': self.report_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }

