from datetime import datetime
from app import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    answers = db.relationship('Answer', backref='user', lazy=True)
    level = db.Column(db.String(20), nullable=True, default='Easy')
    nb_attempts = db.Column(db.Integer, nullable=True, default=0)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    def add_answer(self, answer_text, is_correct):
        answer = Answer(answer=answer_text, is_correct=is_correct, user_id=self.id)
        db.session.add(answer)
        db.session.commit()
    def get_level(self):
        correct_answers = Answer.query.filter_by(user_id=self.id, is_correct=True).count()
        if correct_answers == 2:
            level = "Medium"
        elif correct_answers == 3:
            level = "Hard"
        else:
            level = "Easy"
        return level
    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.answer}', '{self.is_correct}')"




    



