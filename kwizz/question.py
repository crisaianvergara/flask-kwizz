from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.exceptions import abort

from kwizz.auth import login_required
from kwizz.db import get_db

bp = Blueprint("question", __name__)

@bp.route("/")
def index():
    db = get_db()
    questions = db.execute(
        """
            SELECT q.id, question, answer, created_on, created_by, username
            FROM question q JOIN user u ON q.created_by = u.id
            ORDER BY created_by DESC
        """
    ).fetchall()
    return render_template("question/index.html", questions=questions)

@bp.route("/create/", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        error = None

        if not question:
            error = "Question is required."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO question (question, answer, created_by)"
                " VALUES (?, ?, ?)",
                (question, answer, g.user["id"])
            )
            db.commit()
            return redirect(url_for("question.index"))
    
    return render_template("question/create.html")

def get_question(id, check_creator=True):
    question = get_db().execute(
        """
            SELECT q.id, question, answer, created_on, created_by, username
            FROM question q JOIN user u ON q.created_by = u.id
            WHERE q.id = ?
        """,
        (id,)
    ).fetchone()

    if question is None:
        abort(404, f"Question id {id} doesn't exist.")

    if check_creator and question["created_by"] != g.user['id']:
        abort(403)
    
    return question

@bp.route("/<int:id>/update/", methods=("GET", "POST"))
@login_required
def update(id):
    question = get_question(id)

    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        error = None

        if not question:
            error = "Question is required."

        if error is not  None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                    UPDATE question SET question = ?, answer = ?
                    WHERE id = ?
                """,
                (question, answer, id)
            )
            db.commit()
            return redirect(url_for("question.index"))
    
    return render_template("question/update.html", question=question)

@bp.route("/<int:id>/delete/", methods=("POST",))
@login_required
def delete(id):
    get_question(id)
    db = get_db()
    db.execute("DELETE FROM question WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("question.index"))