Author
Deepanshu Shrivasatv
22f2000243
22f2000243@ds.study.iitm.ac.in

About Me:
I am studying BSc in Data Science from IIT Madras, I love learning and exploring in the technology field. I know some of the programming language like Python, Java. I have made several different projects. I am also passionate about learning Artificial intelligence and machine learning.

Description
The Quiz Master App is an interactive application designed to create, manage, and play quizzes. It allows users to add questions, set answer choices, and track scores. The app can be used for learning, entertainment, or competitive quizzes. It may support different question types (MCQs, true/false, or short answers) and could include features like timers, leaderboards, and performance analytics. Whether for self-study, classroom use, or fun challenges, the app makes quizzing engaging and efficient.

Technologies used
1) Flask: Flask Framework used in backend for building the web application.
2) SQL Alchemy: ORM (Object-Relational Mapping) tool for database interactions.
3) SQLite: Database management system for storing application data.
4) HTML/CSS & bootstrap : User interface is designed using html/css and for styling of webpages bootstrap is used
5) Jinja2: Template for rendering dynamic HTML pages
6) Python libraries: various libraries are used to enhance functionalities, including “Datetime” for date and time operations, “Matplotlib” for creating charts for different users.


DB Schema Design
	•	User: Stores user details like id, email, password, role (admin/student), name, etc.
	•	Linked to Score (users participate in quizzes).
	•	Course: Contains id, course_name, and description.
	•	Linked to Chapter (a course has multiple chapters).
	•	Chapter: Includes id, chapter_name, topics, and total_question.
	•	Linked to Course and Question (chapters contain questions).
	•	Linked to Quiz (quizzes are based on chapters).
	•	Question: Holds question details like id, chapter_id, question_title, options, and correct answers.
	•	Linked to Chapter.
	•	Quiz: Contains quiz information like id, chapter_id, quiz_date, and time_duration.
	•	Linked to Chapter and Score.
	•	Score: Tracks quiz results with fields like id, quiz_id, user_id, and the user's score.
	•	Linked to User and Quiz.
Relationships
	•	A User takes a quiz and has a corresponding score.
	•	A Course contains multiple chapters, each having questions.
	•	A Quiz is tied to a chapter, and scores are recorded for users who attempt it.

Video
<<Link to your online video of not more than 3 minutes length>>
