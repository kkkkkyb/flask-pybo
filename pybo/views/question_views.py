from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from sqlalchemy import func

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer, User, question_voter
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1) # GET 방식으로 요청한 URL 에서 page 값을 가져온다
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    # 추천순 : 추천을 많이 받은 질문을 먼저 보여줌
    if so == 'recommend':
        # 추천순으로 정렬하기 위해선 각 질문을 추천한 사람들의 수를 알아야 하는데
        # 추천한 사람들의 수를 알기 위해서 서브쿼리를 사용함
        # 서브쿼리를 정의할 때 추천을 받은 질문의 아이디끼리 그룹으로 묶어 개수를 셈

        # 질문을 추천한 사람들의 아이디를 가져옴(아우터조인 시 Question 객체와 연결시키기 위함)
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
                    .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
                        .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
                        .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    # 인기순 : 질문에 등록된 답변이 많은 질문을 먼저 보여줌
    elif so == 'popular':
        # 인기순으로 정렬하기 위해선 각 질문에 달린 답변의 수를 알아야 하는데
        # 답변한 사람들의 수를 알기 위해서 서브쿼리를 사용함
        # 서브쿼리를 정의할 때 답변을 단 질문의 아이디로 그룹을 묶어 개수를 셈

        # 답변을 단 질문의 아이디를 가져옴(아우터조인 시 Question 객체와 연결시키기 위함)
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
                    .group_by(Answer.question_id).subquery()
        question_list = Question.query \
                        .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
                        .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    # 최신순 : 날짜순
    else:
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        # 답변을 단 질문의 아이디(아우터조인 시 Question 객체와 연결시키기 위함), 답변의 내용, 작성자를 가져옴
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
                    .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
                        .join(User) \
                        .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                        .filter(Question.subject.ilike(search) | # 질문제목
                                Question.content.ilike(search) | # 질문내용
                                User.username.ilike(search) | # 질문작성자
                                sub_query.c.content.ilike(search) | # 답변내용
                                sub_query.c.username.ilike(search) # 답변작성자
                        ) \
                        .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=10) # Pagination 객체로 반환
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, sp=so)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()

    # POST 방식으로 들어올 경우(질문 저장) 해당 if 문을 실행하고 질문 리스트를 보여준다
    # form.validate_on_submit() : POST 방식으로 전송된 폼 데이터의 적합성을 점검한다
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))

    # GET 방식으로 들어올 경우(질문 등록 버튼 클릭) 질문 게시판 폼을 보여준다
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('question._list'))

