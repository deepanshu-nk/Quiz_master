from flask import Flask,render_template,request,url_for,redirect,flash,session 
from .models import * 
from flask import current_app as app
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 


@app.route("/")
def home():
    return render_template("test.html")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        Qyalification = request.form.get("Qyalification")
        DOB = request.form.get("DOB")
        dob_datetime = datetime.strptime(DOB, "%Y-%m-%d")
        user = User_detail.query.filter_by(email=email).first()
        
        if user:
            return render_template("registeration.html",message="User already exist")
        new_user = User_detail(email=email,password=password,name=name,Qyalification=Qyalification,DOB=dob_datetime)
        db.session.add(new_user)
        db.session.commit()

        # Store user session after registration
        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_email"] = new_user.email
        session["user_role"] = new_user.role

        return render_template("login.html")
    return render_template("registeration.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User_detail.query.filter_by(email=email,password=password).first()
        session["user_id"] = user.id
        if user and user.role=="User":
            return redirect(url_for("user_deshbord",name=email))
        elif user and user.role=="Admin":
            return redirect(url_for("admin_deshbord",name=email))
        else:
            return render_template("login.html",message="Invalid login")
    return render_template("login.html")



@app.route("/add_course/<name>",methods=["GET","POST"])
def course(name):
    if request.method=="POST":
        course_name = request.form.get("course_name")
        description = request.form.get("description")
        course = Course_detail.query.filter_by(course_name=course_name).first()
        if course:
            return render_template("Add_course.html",message="course allredy registered")
        new_course = Course_detail(course_name=course_name,description=description)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("admin_deshbord",name=name))
    return render_template("Add_course.html",name=name)

@app.route("/edit_course/<id>/<name>",methods=["GET","POST"])
def edit_course(id,name):
    cour = Course_detail.query.filter_by(id=id).first()
    if request.method=="POST":
        course_name = request.form.get("course_name")
        Description = request.form.get("description")

        cour.course_name = course_name
        cour.description = Description
        db.session.commit()
        return redirect(url_for("admin_deshbord", name=name))

    return render_template("Edit_course.html",cour=cour,name=name) 

@app.route("/delete_course/<id>/<name>",methods=["GET","POST"])
def dlt(id,name):
    course = Course_detail.query.filter_by(id=id).first()
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("admin_deshbord",name=name))


@app.route("/add_chapter/<course_id>/<course_name>/<name>",methods=["GET","POST"])
def add_chapter(course_id,course_name,name):
    if request.method=="POST":
        Chapter_name=request.form.get("Chapter_names")
        Topics = request.form.get("Topics")
        Question = request.form.get("Questions")
        new_chapter = Chapter(Chapter_name=Chapter_name,Topics=Topics,Question=Question,course_id=course_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("admin_deshbord",name=name))
    return render_template("Add_chapter.html",course_id=course_id,course_name=course_name,name=name)

@app.route("/edit/<id>/<name>", methods=["GET", "POST"])
def get(id, name):
    C = Chapter.query.filter_by(id=id).first()  # Corrected `.first()`
    if not C:  # Check if the chapter exists
        return "Chapter not found", 404

    if request.method == "POST":
        Chapter_name = request.form.get("Chapter_name")
        Topics = request.form.get("Topics")
        Question = request.form.get("Question")
        
        # Update the chapter's details
        C.Chapter_name = Chapter_name
        C.Topics = Topics
        C.Question = Question

        # Save changes to the database
        db.session.commit()
        return redirect(url_for("admin_deshbord", name=name))
   
    # Render the edit page
    return render_template("Edit_chapter.html", chapter=C, name=name)

@app.route("/delete/<id>/<name>",methods=["GET","POST"])
def delete(id,name):
    c = Chapter.query.filter_by(id=id).first()
    if not c:
        return "chapter not found"
    else:
        db.session.delete(c)
        db.session.commit()
    return redirect(url_for("admin_deshbord", name=name))

@app.route("/delets/<id>/<name>",methods=["GET","POST"])
def delets(id,name):
    q = Question.query.filter_by(id=id).first()
    if not q:
        return "Qestion not found"
    else:
        db.session.delete(q)
        db.session.commit()
    return redirect(url_for("admin_deshbord", name=name))

# 🟢 Route to create a new quiz
@app.route("/quiz/<name>",methods=["GET","POST"])
def quiz(name):
    Chapters = Chapter.query.all()
    return render_template("Quiz.html",Chapters=Chapters,name=name)



@app.route('/add_quiz/<chapter_id>', methods=['GET', 'POST'])
def ass_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    Chapters = Chapter.query.all()
    if request.method == 'POST':
        quiz_date = datetime.strptime(request.form['quiz_date'], "%Y-%m-%d")
        time_duration = datetime.strptime(request.form['time_duration'], "%H:%M").time()
        feedback = request.form['feedback']
        
        existing_quiz = Quizs.query.filter_by(chapter_id=chapter_id,quiz_date=quiz_date).first()
        if existing_quiz:
            return render_template("Add_quiz.html",msg="Quiz Already Registerd")
        new_quiz = Quizs(chapter_id=chapter_id, quiz_date=quiz_date, time_duration=time_duration, feedback=feedback)
        db.session.add(new_quiz)
        db.session.commit()
        return render_template("Quiz.html",Chapters=Chapters)
    return render_template('Add_quiz.html',chapter=chapter)


@app.route('/add_question/<chapter_id>/<chapter_name>', methods=['GET', 'POST'])
def add_question(chapter_id,chapter_name):
    Chapters = Chapter.query.all()
    if request.method == 'POST':
        question_title = request.form['question_title']
        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        new_question = Question(
            chapter_id=chapter_id,
            question_title=question_title,
            question_statement=question_statement,
            option_1=option1,
            option_2=option2,
            option_3=option3,
            option_4=option4,
            answers=correct_option
        )
        db.session.add(new_question)
        db.session.commit()
        return render_template("Quiz.html",Chapters=Chapters)
    return render_template('Question.html',chapter_id=chapter_id,chapter_name=chapter_name)

@app.route("/View_Quiz/<id>/<name>")
def view(id,name):
    quiz = Quizs.query.get_or_404(id)
    chapter = Chapter.query.get(quiz.chapter_id)
    course = Course_detail.query.get(chapter.course_id)
    return render_template("View_Quiz.html",name=name,quiz=quiz.id,course_name=course.course_name,chapter=chapter.Chapter_name,Ques=chapter.Question,date=quiz.quiz_date,time=quiz.time_duration)

@app.route("/submit_exam/<quiz_id>/<name>",methods=["GET","POST"])
def exam(quiz_id,name):
    questions = Question.query.all()
    quiz = Quizs.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(chapter_id=quiz.chapter_id).all()
    
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for('signin'))
    
    user = User_detail.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('signup'))

    if request.method=="POST":     
        score = 0
        total_question = len(questions)

        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer and user_answer == question.answers:
                score += 1

        quiz_score = Score(quiz_id=quiz_id,user_id=user_id,score=score)
        db.session.add(quiz_score)
        db.session.commit()
        flash(f'Quiz Submitted! You scored {score}/{total_question}', 'success')
        return redirect(url_for("user_deshbord",name=user.name,id=user.id))

    return render_template("Exam.html",questions=questions,name=name)

#User serach 
@app.route("/search/<name>", methods=["GET", "POST"])
def search(name):
    if request.method == "POST":
        search_txt = request.form.get("search_txt")
        course = fetch_course(search_txt) or fetch_chapter(search_txt)
        return render_template("Admin_deshbord.html", name=name, course=course)



@app.route("/user_search/<name>", methods=["GET", "POST"])
def user_search(name):
    if request.method == "POST":
        search_txt = request.form.get("search_txt")
        course = fetch_course(search_txt) or fetch_chapter(search_txt)
        return render_template("User_deshbord.html", name=name, course=course)

    



@app.route("/scores/<name>")
def scores(name):
    # Check if the user is logged in
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("signin"))

    # Fetch user details
    user = User_detail.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("signin"))

    # Fetch scores with related course and chapter data
    scores = (
        db.session.query(
            Score.id,
            Score.score,
            Quizs.quiz_date,
            Chapter.Chapter_name,
            Chapter.Question,
            Course_detail.course_name
        )
        .join(Quizs, Score.quiz_id == Quizs.id)
        .join(Chapter, Quizs.chapter_id == Chapter.id)
        .join(Course_detail, Chapter.course_id == Course_detail.id)
        .filter(Score.user_id == user_id)
        .all()
    )

    return render_template("score.html", scores=scores, user=user,name=name)


@app.route("/admin/<name>")
def admin_deshbord(name):
    course = get_course()
    return render_template("Admin_deshbord.html",name=name,course=course)

@app.route("/user/<name>")
def user_deshbord(name):
    course = get_course()
    chapter = get_chapter()
    quizzes = Quizs.query.filter_by(id=id).first
    return render_template("User_deshbord.html",name=name,course=course,chapter=chapter,quizzes=quizzes)


def get_course():
    courses = Course_detail.query.all()
    return courses

def get_chapter():
    chapters = Chapter.query.all()
    return chapters

def get_quiz(id):
    quiz = Quizs.query.filter_by(id=id).first
    return quiz

def fetch_course(search_txt):
    courses = Course_detail.query.filter(Course_detail.course_name.ilike(f"%{search_txt}%")).all()
    return courses

def fetch_chapter(search_txt):
    chapters = Chapter.query.filter(Chapter.Chapter_name.ilike(f"%{search_txt}%")).all()
    return chapters


@app.route("/admin_summery/<name>")
def summery(name):
    # Generate graph and save it
    generate_graph()
    
    return render_template("Admin_summery.html", name=name)


def generate_graph():
    Chapter = get_chapter()  # Assuming this function fetches chapter data
    
    # Extract data
    summery = {c.Chapter_name: c.Question for c in Chapter}
    
    # Prepare graph data
    x_chapter = list(summery.keys())
    y_question = list(summery.values())

    # Create Bar Chart
    plt.figure(figsize=(7,5))
    plt.bar(x_chapter, y_question, color="blue", width=0.4)
    plt.title("Chapter vs. Questions")
    plt.xlabel("Chapters")
    plt.ylabel("Number of Questions")
    # Rotate labels for better readability
    
    # Save and clear figure
    plt.savefig("./static/images/admin_summery.png")
    plt.clf()  # Clear plot to prevent overlapping in future calls



@app.route("/user_summery/<name>")
def user_summery(name):
    # Generate the graph for quiz scores per chapter
    generate_graph()
    
    return render_template("User_summery.html", name=name)

def generate_graph():
    # Fetch all chapters
    chapters = Chapter.query.all()
    
    # Prepare data for graph
    chapter_scores = {}

    for chapter in chapters:
        # Fetch all quiz IDs for this chapter
        quiz_ids = [quiz.id for quiz in chapter.quiz]
        
        # Get total score for all users in this chapter
        total_score = db.session.query(db.func.sum(Score.score)).filter(Score.quiz_id.in_(quiz_ids)).scalar() or 0

        # Store the total score per chapter
        chapter_scores[chapter.Chapter_name] = total_score

    # Extract data for plotting
    x_chapter = list(chapter_scores.keys())
    y_scores = list(chapter_scores.values())

    # Create Bar Chart
    plt.figure(figsize=(8, 5))
    plt.bar(x_chapter, y_scores, color="blue", width=0.4)
    plt.title("Quiz score for each chapter")
    plt.xlabel("Chapter")
    plt.ylabel("Scores")

    # Save and clear figure
    plt.savefig("./static/images/user_summery.png")
    plt.clf()  # Clear plot to prevent overlapping in future calls