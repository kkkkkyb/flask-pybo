from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # 데이터베이스 접속 주소
SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트를 처리하는 옵션
SECRET_KEY = "dev"