from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config

# 제약 조건 이름의 규칙을 정의
naming_convention = {
    "ix": 'ix_%(column_0_lable)s',
    "uq": 'uq_%(table_name)s_%(column_0_name)s',
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# create_app은 플라스크 내부에서 정의된 함수명이다. (다른 이름으로 작성할 경우 실행되지 않음)
def create_app():
    app = Flask(__name__)

    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True) # render_as_batch 속성이 False 라면 '제약 조건의 변경을 지원하지 않는다' 는 오류를 발생시킴
    else:
        migrate.init_app(app, db)

    # 모델 정의 파일 불러오기
    from . import models

    # 블루프린트 : 비슷한 동작을 하는 URL 끼리 파일을 묶어서 관리할 수 있음
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp) # 메인페이지
    app.register_blueprint(question_views.bp) # 질문 게시글 관련 URL
    app.register_blueprint(answer_views.bp) # 답변 관련 URL
    app.register_blueprint(auth_views.bp) # 회원가입 관련 URL
    app.register_blueprint(comment_views.bp) # 댓글 관련 URL
    app.register_blueprint(vote_views.bp) # 투표 관련 URL

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app
