from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Subject, db,Chapter,Quiz,Question,Score,User
from datetime import datetime


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()  
    return render_template("admin_dashboard.html", subjects=subjects, chapters=chapters)



@admin_bp.route('/add_subject', methods=['POST'])
def add_subject():
    """Adds a new subject to the database."""
    name = request.form.get('name')
    
    
    if not name:
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400
    
    new_subject = Subject(name=name)
    db.session.add(new_subject)
    db.session.commit()
    
    return jsonify({'status': 'success', 'id': new_subject.id, 'name': new_subject.name})

@admin_bp.route('/add_chapter', methods=['POST'])
def add_chapter():
   
    subject_id = request.form.get('subject_id')
    name = request.form.get('name')
    no_of_questions = request.form.get('no_of_questions')
    
    if not subject_id or not name or not no_of_questions:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'status': 'error', 'message': 'Invalid subject ID'}), 404

        new_chapter = Chapter(name=name, no_of_questions=int(no_of_questions), subject_id=int(subject_id))
        db.session.add(new_chapter)
        db.session.commit()

        return jsonify({'status': 'success', 'id': new_chapter.id, 'name': new_chapter.name, 'no_of_questions': new_chapter.no_of_questions})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@admin_bp.route('/edit_chapter', methods=['POST'])
def edit_chapter():
    chapter_id = request.form['id']
    name = request.form['name']
    no_of_questions = request.form['no_of_questions']

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        chapter.name = name
        chapter.no_of_questions = int(no_of_questions)
        db.session.commit()
        return jsonify({'status': 'success', 'id': chapter.id, 'name': chapter.name, 'no_of_questions': chapter.no_of_questions, 'subject_id': chapter.subject_id})
    return jsonify({'status': 'error', 'message': 'Chapter not found'})



@admin_bp.route('/update_chapter', methods=['POST'])
def update_chapter():
    chapter_id = request.form.get("id")
    name = request.form.get("name")
    no_of_questions = request.form.get("no_of_questions")

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        chapter.name = name
        chapter.no_of_questions = no_of_questions
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Chapter not found"})


@admin_bp.route('/delete_chapter', methods=['POST'])
def delete_chapter():
    chapter_id = request.form.get("id")

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Chapter not found"})

@admin_bp.route('/quiz_management')
def quiz_management():
    subjects = Subject.query.all()  
    return render_template('quiz_management.html', subjects=subjects)

@admin_bp.route('/get_subjects')
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in subjects])

@admin_bp.route('/get_chapters/<int:subject_id>')
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([{"id": c.id, "name": c.name} for c in chapters])

@admin_bp.route('/add_quiz', methods=['POST'])
def add_quiz():
    data = request.json  
    chapter_id = data.get("chapter_id")
    date = data.get("date_of_quiz")
    duration = data.get("time_duration")
    print(chapter_id,date,duration)
    if not chapter_id or not date or not duration:
        return jsonify({"status": "error", "message": "All fields are required!"})

    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format!"})

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"status": "error", "message": "Invalid chapter!"})

    subject = Subject.query.get(chapter.subject_id)
    subject_name = subject.name if subject else "Unknown Subject"

    new_quiz = Quiz(chapter_id=chapter_id, date_of_quiz=date, time_duration=duration)
    db.session.add(new_quiz)
    db.session.commit()
    print("yes")
    return jsonify({
        "status": "success",
        "quiz_id": new_quiz.id,
        "subject_name": subject_name,
        "chapter_id": chapter_id,
        "date_of_quiz": str(date),
        "time_duration": duration
    })

@admin_bp.route('/get_quizzes')
def get_quizzes():
    quizzes = Quiz.query.all()
    
    quiz_list = []
    
    for quiz in quizzes:
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id) if chapter else None
        quiz_list.append({
            "id": quiz.id,
            "chapter_id": quiz.chapter_id,
            "subject_name": subject.name if subject else "Unknown Subject",
            "date_of_quiz": str(quiz.date_of_quiz),
            "time_duration": quiz.time_duration
        })

    return jsonify(quiz_list)

@admin_bp.route('/update_quiz/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    data = request.json
    chapter_id = data.get("chapter_id")
    date_of_quiz = data.get("date_of_quiz")
    time_duration = data.get("time_duration")

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"status": "error", "message": "Quiz not found!"})

    quiz.chapter_id = chapter_id
    quiz.date_of_quiz = date_of_quiz
    quiz.time_duration = time_duration

    db.session.commit()
    return jsonify({"status": "success", "message": "Quiz updated successfully!"})
@admin_bp.route('/update_question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    question = Question.query.get(question_id)
    
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()

    try:
        question.question_title = data.get("question_title", question.question_title)
        question.question_statement = data.get("question_statement", question.question_statement)
        question.option1 = data.get("option1", question.option1)
        question.option2 = data.get("option2", question.option2)
        question.option3 = data.get("option3", question.option3)
        question.option4 = data.get("option4", question.option4)
        question.correct_option = data.get("correct_option", question.correct_option)

        db.session.commit()  

        return jsonify({"message": "Question updated successfully!"})

    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/delete_quiz/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"status": "error", "message": "Quiz not found!"})

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"status": "success", "message": "Quiz deleted successfully!"})


@admin_bp.route('/add_question', methods=['POST'])
def add_question():
    data = request.json
    quiz_id = data.get("quiz_id")
    chapter_id = data.get("chapter_id")
    title = data.get("question_title")
    statement = data.get("question_statement")
    option1 = data.get("option1")
    option2 = data.get("option2")
    option3 = data.get("option3")
    option4 = data.get("option4")
    correct_option = data.get("correct_option")

    new_question = Question(
        quiz_id=quiz_id,
        question_statement=statement,
        question_title=title,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=int(correct_option)
    )

    db.session.add(new_question)
    db.session.commit()
    

    return jsonify({"status": "success", "question_id": new_question.id})

@admin_bp.route('/get_questions/<quiz_id>')
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    return jsonify([
        {
            "id": q.id,
            "question_title": q.question_title  
        } 
        for q in questions
    ])
@admin_bp.route('/get_question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

  
    return jsonify({
        "id": question.id,
        "quiz_id": question.quiz_id,
        "question_title": question.question_title,
        "question_statement": question.question_statement,
        "option1": question.option1,
        "option2": question.option2,
        "option3": question.option3,
        "option4": question.option4,
        "correct_option": question.correct_option
    })



@admin_bp.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({"status": "success", "message": "Question deleted successfully!"})
    else:
        return jsonify({"status": "error", "message": "Question not found"}), 404


@admin_bp.route('/delete_subject', methods=['POST'])
def delete_subject():
    subject_id = request.form.get('id')
    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({"status": "error", "message": "Subject not found!"})

    try:
        Chapter.query.filter_by(subject_id=subject_id).delete()

        db.session.delete(subject)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})
    

@admin_bp.route('/scores')
def view_scores():
    scores = db.session.query(
        Score.id,
        User.id.label("user_id"),
        User.full_name,
        Quiz.id.label("quiz_id"),
        Quiz.date_of_quiz,
        Score.total_score,
        Subject.name.label("subject_name"),
        Chapter.name.label("chapter_name")
    ).join(User, User.id == Score.user_id
    ).join(Quiz, Quiz.id == Score.quiz_id
    ).join(Chapter, Chapter.id == Quiz.chapter_id
    ).join(Subject, Subject.id == Chapter.subject_id
    ).all()

    return render_template("/view_scores.html", scores=scores)



@admin_bp.route('/base')
def base():
    return render_template("base.html")


