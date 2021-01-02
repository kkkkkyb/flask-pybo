from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST', ))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    # 입력값이 존재할 경우
    if form.validate_on_submit():
        content = request.form['content'] # request : form 에서 전달된 객체
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))

    # 입력값이 존재하지 않을 경우
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modity/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if g.user != answer.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)

    return redirect('{}.#answer_{}'.format(url_for('question.detail', quesiton_id=answer.question.id), answer.id))

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id

    if g.user != answer.user:
        flash('삭제 권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))

