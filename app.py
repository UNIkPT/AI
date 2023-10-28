from flask import Flask, request, render_template_string, session
from models import AI

app = Flask(__name__)
app.secret_key = "brad0809"

@app.route("/", methods=["GET", "POST"])
def index():
    session.permanent = True
    
    # 앱을 처음 실행했을 때만 session을 초기화
    if 'initialized' not in session:
        session.clear()
        session['initialized'] = True

    result = ""
    image_url = ""
    translated_text=""
    original_result=""
    first_feedback=""

    if 'conversation' not in session:
        session['conversation'] = []
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        input_type = request.form.get("input_type", "")
        if user_input == "clear":
            session.clear()
            print('clear')
            
        if input_type == "text":
            original_prompt = user_input

            if 'first_input' not in session:
                session['first_input'] = True  # 첫 번째 입력임을 나타냅니다.
                session['original_prompt'] = user_input
                session['original_result'] = AI.chatgpt(original_prompt)
                session['first_feedback'] = AI.feedback_chatgpt(original_prompt, session['conversation'])


            else:
                feedback = AI.feedback_chatgpt(user_input, session['conversation'])
                result = feedback
                session['conversation'].extend([
                    {"role": "user", "content": user_input},
                    {"role": "system", "content": result}
                ])
            
        elif input_type == "image":
            translated_text, image_url = AI.dalle(user_input)
    print(session['conversation'])
    return render_template_string('''
    <form action="/" method="post">
        Select input type: 
        <input type="radio" name="input_type" value="text" checked> Text
        <input type="radio" name="input_type" value="image"> Image
        <br><br>
        Enter your prompt: <br>
        <textarea name="user_input" rows="4" cols="50"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    {% if session.get('first_input') %}
    <br>
        <h3>Original Prompt</h3>
        <p>{{ session['original_prompt'] }}</p>
        <h3>Original Prompt Result</h3>
        <p>{{ session['original_result'] }}</p>
        <h3>Feedback</h3>
        <p>{{ session['first_feedback'] }}


        {% for message in session['conversation'] %}
            <div class="{{ message['role'] }}">
                {% if message['role']=='user' %}
                    <h3>User:</h3>
                {% elif message['role']=='system' %}
                    <h3>Feedback:</h3>
                {% endif %}
                <p>{{ message['content'] }}</p>
            </div>
        {% endfor %}

    {% elif translated_text %}
    <br>
    <h3>Input Prompt : </h3>
    <p>{{ translated_text }}</p>
    <img src="{{ image_url }}" alt="Generated Image">
    {% endif %}
    ''', translated_text=translated_text, image_url=image_url, original_result=original_result,first_feedback=first_feedback, result=result)


if __name__ == '__main__':
    app.run(debug=True)