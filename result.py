from flask import Flask, render_template, request
from flask_caching import Cache
import GetData, cache_config

app = Flask(__name__)
app.config.from_mapping(cache_config.config)
cache = Cache(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_cache_key(user_id): # 캐시 키 생성 함수
    return f"crawling_result_{user_id}"

@app.route('/result', methods=['POST'])
def result():
    user_id = request.form['user_id']
    password = request.form['password']
    cache_key = get_cache_key(user_id) # 캐시 키 저장

    # 캐시에서 결과를 시도하여 가져옵니다.
    cached_result = cache.get(cache_key)
    if cached_result is not None: # 캐시된 결과가 있다면, 캐시된 값으로부터 데이터를 로드
        course_info, total_credits, require_credit, require_cultural, consulting_total, consulting_detail = cached_result

    else:
        # 캐시된 결과가 없다면, 크롤링을 실행하고 캐시에 저장
        course_info = {'교필': 0, '교선1': 0, '교선2': 0, '교선3': 0, '교선4': 0, '교선5': 0, '교선6': 0, '교선7': 0, '교선8': 0, '전필': 0, '전선': 0, '부전1': 0, '복전1': 0, '일선': 0}

        crawling_data, require_credit, require_cultural, consulting_total, consulting_detail = GetData.crawling_main(user_id, password)
        for course_name, course_details in crawling_data.items():
            if course_name in course_info:  # 안전한 값 추가를 위해 확인
                course_info[course_name] += int(course_details['학점'])
        total_credits = sum(course_info.values())
        # 결과를 캐시에 저장
        cache.set(cache_key, (course_info, total_credits, require_credit, require_cultural, consulting_total, consulting_detail))

    return render_template('result.html', course_info=course_info, total_credits=total_credits, require_credit = require_credit, require_cultural = require_cultural, consulting_total = consulting_total, consulting_detail = consulting_detail)

if __name__ == '__main__':
    app.run(debug=True)