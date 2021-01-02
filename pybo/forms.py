
# 질문, 답변 폼 형식을 정의하는 파일( 파이썬 코드 내에서 사용 )

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# 질문 폼 형식 정의하는 함수
class QuestionForm(FlaskForm):
    # 모델 클래스 속성(라벨, 필드값 검증 도구)
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

# 답변 폼 형식 정의하는 함수
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

# 사용자(회원가입) 폼 형식 정의하는 함수
class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(), Email()]) # Email() : 이메일 형식인지 검사

# 로그인 폼 형식 정의하는 함수
class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

# 질문 댓글 폼 형식 정의하는 함수
class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])

