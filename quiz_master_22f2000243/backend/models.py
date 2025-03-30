from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_detail(db.Model):
    __tablename__="user_detail"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String,default="User") 
    name=db.Column(db.String,nullable=False)
    Qyalification=db.Column(db.String,nullable=False)
    DOB=db.Column(db.Integer,nullable=False)

class Course_detail(db.Model):
    __tablename__="course_detail"
    id=db.Column(db.Integer,primary_key=True)
    course_name = db.Column(db.String,unique=True,nullable=False)
    description=db.Column(db.String,nullable=False)
    chapter=db.relationship("Chapter",cascade="all,delete",backref="course_detail",lazy=True)

class Chapter(db.Model):
    __tablename__="chapter_detail"
    id=db.Column(db.Integer,primary_key=True)
    Chapter_name=db.Column(db.String,unique=True,nullable=False)
    Topics = db.Column(db.String,nullable=False)
    Question = db.Column(db.Integer,nullable=False)
    chapter_pic_url = db.Column(db.String,nullable=True,default="None")
    course_id = db.Column(db.Integer,db.ForeignKey("course_detail.id"),nullable=False)
    quiz = db.relationship("Quizs",cascade="all,delete",backref="chapter_detail",lazy=True)
    question = db.relationship("Question",cascade="all,delete",backref="chapter_detail",lazy=True)

class Quizs(db.Model):
    __tablename__="quizs"
    id = db.Column(db.Integer,primary_key=True)
    chapter_id = db.Column(db.Integer,db.ForeignKey("chapter_detail.id"),nullable=False)
    quiz_date = db.Column(db.Date,nullable=False)
    time_duration = db.Column(db.Time,nullable=True)
    feedback = db.Column(db.String,nullable=False)


class Question(db.Model):
    __tablename__="question"
    id = db.Column(db.Integer,primary_key=True)
    chapter_id = db.Column(db.Integer,db.ForeignKey("chapter_detail.id"),nullable=False)
    question_title = db.Column(db.String,nullable=False)
    question_statement=db.Column(db.String,unique=True,nullable=False)
    option_1 = db.Column(db.String,nullable=True)
    option_2 = db.Column(db.String,nullable=True)
    option_3 = db.Column(db.String,nullable=True)
    option_4 = db.Column(db.String,nullable=True)
    answers = db.Column(db.String,nullable=True)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizs.id"), nullable=False)  # Fixed foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user_detail.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)   





