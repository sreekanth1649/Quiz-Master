from flask import Blueprint, render_template, session, Flask, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import Score, Quiz, Chapter, db, Subject, Question
from datetime import date

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():

    upcoming_quizzes = (
        db.session.query(
            Quiz.id, Chapter.no_of_questions, Quiz.date_of_quiz, Quiz.time_duration,
            Subject.name.label('subject_name'), Chapter.name.label('chapter_name')
        )
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .join(Subject, Chapter.subject_id == Subject.id)
        .filter(Quiz.date_of_quiz >= date.today())
        .all()
    )

    quizzes = [
        {
            "id": quiz.id,
            "no_of_questions": quiz.no_of_questions,
            "date_of_quiz": quiz.date_of_quiz,
            "time_duration": quiz.time_duration,
            "subject_name": quiz.subject_name,
            "chapter_name": quiz.chapter_name
        }
        for quiz in upcoming_quizzes
    ]

    return render_template('user_dashboard.html', quizzes=quizzes)


@user_bp.route('/submit_answer', methods=['POST'])
def submit_answer():
    quiz_id = session.get('quiz_id')
    current_question = session.get('current_question', 0)

    selected_option = request.form.get('selected_option')
    if not selected_option:
        return redirect(url_for('user.quiz_question', quiz_id=quiz_id))


    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)

    if not questions or current_question >= total_questions:
        return redirect(url_for('user.quiz_result', quiz_id=quiz_id))


    correct_option = questions[current_question].correct_option.strip()  
    sc=0

    if selected_option == correct_option:
        sc+=1
        session['score'] = session.get('score', 0) + 1

    print("score izzz:",sc)

    session['current_question'] = current_question + 1


    if session['current_question'] < total_questions:
        return redirect(url_for('user.quiz_question', quiz_id=quiz_id))
    
    return redirect(url_for('user.quiz_result', quiz_id=quiz_id))


@user_bp.route('/get_quiz/<int:quiz_id>', methods=['GET'])
def get_quiz_details(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    chapter = quiz.chapter
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    subject = chapter.subject
    if not subject:
        return jsonify({"error": "Subject not found"}), 404


    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    return jsonify({
        "quiz": {
            "id": quiz.id,
            "subject_name": subject.name,  
            "chapter_name": chapter.name,  
            "num_questions": chapter.no_of_questions,  
            "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d") if quiz.date_of_quiz else "Not Set",
            "time_duration": quiz.time_duration
        },
        "questions": [
            {"id": q.id, "question_title": q.question_title} for q in questions
        ]
    })

@user_bp.route('/start_quiz/<int:quiz_id>', methods=['GET'])
def start_quiz(quiz_id):
    session['quiz_id'] = quiz_id
    session['current_question'] = 0
    session['score'] = 0
    return redirect(url_for('user.quiz_question', quiz_id=quiz_id))

@user_bp.route('/quiz_question/<int:quiz_id>', methods=['GET'])

def quiz_question(quiz_id):
    if 'current_question' not in session:
        return redirect(url_for('user.dashboard'))  


    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for('user.dashboard'))  

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)

    if session['current_question'] >= total_questions:
        return redirect(url_for('user.quiz_result', quiz_id=quiz_id))

    question = questions[session['current_question']]
    
    print("Current user is:", current_user)

    return render_template('quiz_interface.html', 
                           question=question, 
                           total_questions=total_questions,
                           current_question=session['current_question'] + 1,
                           quiz_id=quiz_id,
                           time_duration=quiz.time_duration,  
                           user=current_user)




@user_bp.route('/quiz_result/<int:quiz_id>', methods=['GET'])
def quiz_result(quiz_id):
    total_score = session.get('score', 0)
    user_id = current_user.id 

    if user_id:
        existing_score = Score.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        if not existing_score:
            score_entry = Score(quiz_id=quiz_id, user_id=user_id, total_score=total_score)
            db.session.add(score_entry)
            db.session.commit()

    print("parsed here")
    return render_template('quiz_result.html', total_score=total_score)


@user_bp.route('/scores', methods=['GET'])
def scores():
    user_id = current_user.id


    user_scores = (
        db.session.query(
            Score.total_score,
            Quiz.date_of_quiz,
            Chapter.no_of_questions
        )
        .join(Quiz, Score.quiz_id == Quiz.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .filter(Score.user_id == user_id)
        .order_by(Quiz.date_of_quiz.desc())  
        .all()
    )

    return render_template('scores.html', scores=user_scores)