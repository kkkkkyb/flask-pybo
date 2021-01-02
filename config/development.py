from config.default import *
from logging.config import dictConfig

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # 데이터베이스 접속 주소
SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트를 처리하는 옵션
SECRET_KEY = "dev"

# 파이보 배포 시 아래 코드를 config\production.py 에 추가할 것

'''
dictConfig({
    'version' : 1, # logging 모듈의 버전을 1로 설정, 업데이트 되어도 현재 설정을 유지한다
    'formatters' : {
        'default' : {
            # asctime : 현재 시간
            # levelname : 로그의 레벨 (debug, info, warning, error, critical)
            # module : 로그를 호출한 모듈명
            # message : 출력 내용
            'format' : '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers' : { # 로그를 출력할 방법을 정의
        'file' : { # 'file' 이라는 이름의 핸들러 정의
            'level' : 'INFO', # 출력 로그 레벨
            'class' : 'logging.handlers.RotatingFileHandler', # 로그 핸들러 클래스, 파일크기가 설정값보다 커지면 파일 뒤에 인덱스 붙여 백업
            'filename' : os.path.join(BASE_DIR, 'logs/myproject.log'), # 로그 파일명
            'maxBytes' : 1024 * 1024 * 5, # 로그 파일 크기, 5 MB
            'backupCount' : 5, # 로그 파일의 개수(5개로 유지)
            'formatter' : 'default', # 포맷터
        },
    },
    'root' : { # 최상위 로거
        'level' : 'INFO',
        'handlers' : ['file']
    }
})
'''
