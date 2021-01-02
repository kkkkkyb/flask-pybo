
# 입력받은 value 를 fmt 형식으로 바꾸는 함수
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)