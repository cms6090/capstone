from flask import Flask, render_template, request
import GetData

app = Flask(__name__)
course_info = {
    '교필': 0,
    '교선': 0,
    '전필': 0,
    '전선': 0,
    '복전': 0,
    '부전': 0,
    '일선': 0
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_id = request.form['user_id']
    password = request.form['password']
    crawling_data = GetData.Crawling(user_id, password)
    
    # for course_name, course_details in crawling_data.items():
    #     print(course_name + ":")
    #     for key, value in course_details.items():
    #         print(key, value)
    
    
    for course_name, course_details in crawling_data.items():
            if(len(course_name) > 2):
                course_name = course_name[0:2]
            course_info[course_name] += int(course_details['학점'])
    total_credits = sum(course_info.values())
    #return render_template('result.html')
    return render_template('result.html', course_info=course_info, total_credits=total_credits)

if __name__ == '__main__':
    app.run(debug=True)
