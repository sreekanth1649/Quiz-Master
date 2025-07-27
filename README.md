# Quiz Master - Modern Application Development I (Jan 2025)

## 📘 Project Overview

**Quiz Master ** is a multi-user web application developed as part of the *Modern Application Development I* course. It functions as an exam preparation platform where users can take quizzes on various subjects and chapters. The application supports two user roles: **Admin (Quiz Master)** and **Users**. Admin has complete control over the subjects, chapters, quizzes, and user management, while users can register, log in, and attempt quizzes of their choice.

---

## 🔧 Tech Stack Used

- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML5, CSS3, Bootstrap
- **Database**: SQLite (Programmatically created)
- **Charting Library**: Chart.js (for visual summaries)
- **Optional**: Flask-Login (for session management), JavaScript (for client-side validation)

---

## 👤 Roles and Functionalities

### 🛡️ Admin (Quiz Master)
- Pre-created admin account (no registration required)
- Add/edit/delete subjects and chapters
- Create quizzes with MCQs (single correct option)
- Schedule quiz with date and time duration
- Manage and search users/quizzes/subjects
- View performance summary with charts

### 👨‍🎓 User
- Register and login with email and password
- View and choose available quizzes
- Attempt quizzes and view scores
- Track previous quiz attempts and performance (charts)

---

## 🗃️ Key Entities and Tables

- **User**: Stores user registration details
- **Subject**: Field of study
- **Chapter**: Subtopics under a subject
- **Quiz**: Quiz under a chapter with time and date
- **Question**: MCQs with one correct option
- **Score**: User attempt and result record

---

## 🌐 API Endpoints (If implemented)
- `/api/subjects` - Get all subjects
- `/api/chapters/<subject_id>` - Get chapters for a subject
- `/api/quizzes/<chapter_id>` - Get quizzes for a chapter
- `/api/results/<user_id>` - Get user's quiz results


