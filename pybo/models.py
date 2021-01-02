
# 데이터 모델을 정의하는 파일( DATABASE 연동 )

from pybo import db

# 계정과 질문이 한 쌍을 이루는 테이블 객체(다대다 관계를 정의하기 위해 db.Table 클래스로 정의되는 객체)
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

# 질문 게시글 데이터 모델
class Question(db.Model):
    # 플라스크는 데이터 타입이 db.Interger 이고 기본키로 지정한 속성은
    # 값이 자동으로 증가하는 특징이 있어서 데이터를 저장할 떄 해당 속성값을 지정하지 않아도
    # 1씩 자동으로 증가하여 저장된다.
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set')) # Question 모델에서 User 모델을 참조하기 위한 필드
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_vote_set'))
    # secondary : 해당 변수(voter)가 다대다 관계이며, question_voter 테이블을 참조함
    # backref : 역참조할떄 사용, 이름이 중복되면 안된다(question_vote_set 중복 사용 X)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

# 답변 게시글 데이터 모델
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) # 질문 삭제 시 답변도 같이 삭제됨됨
    question = db.relationship('Question', backref=db.backref('answer_set')) # db.relationship(참조할 모델, 역참조 설정)
    # 역참조 설정을 해두면 Answer 객체에서 일방적으로 Question 객체를 참조하는 경우라도 그 반대의 참조도 가능해진다(Question 객체에서 Answer 객체 참조 가능)
    # answer_set : 역참조 할 경우 사용하는 키워드
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

# 사용자 데이터 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id 값은 자동으로 증가하는 User 모델의 기본키
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 댓글 데이터 모델
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    # 댓글은 질문 혹은 답변 둘 중 하나에 달 수 있으므로 널이 가능해야 한다
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

