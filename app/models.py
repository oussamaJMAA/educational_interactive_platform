from datetime import datetime
from app import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    role = db.Column(db.String(20), unique=False, nullable=True,default='student')
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
    def get_level(self, curr_level):
        recent_answers = Answer.query.filter_by(user_id=self.id).order_by(Answer.timestamp.desc()).limit(3).all()
        correct_answers = sum(1 for ans in recent_answers if ans.is_correct)
        if curr_level == "Hard":
            if correct_answers == 3:
                level = "Hard"
            elif correct_answers == 2:
                level = "Hard"
            else:
                level = "Medium"
        elif curr_level == "Medium":
            if correct_answers == 3:
                level = "Hard"
            elif correct_answers == 2:
                level = "Medium"
            else:
                level = "Easy"
        elif curr_level == "Easy":
            if correct_answers == 3:
                level = "Medium"
            else:
                level = "Easy"
        return level
    
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Question('{self.question_text}')"





    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Answer('{self.answer}', '{self.is_correct}')"


    

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_text = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"Fedback('{self.feedback_text}', '{self.question_id}','{self.type}')"


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_text = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=True)
    profession = db.Column(db.String(20), nullable=True)
    user = db.relationship('User', backref='reviews')
    def __repr__(self):
        return f"Reviews('{self.review_text}', '{self.question_id}','{self.type}')"



