
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def math():
    a = request.form.get('a')
    b = request.form.get('b')
    operator = request.form.get('operator')
    result = 0 
    if operator == '+':
        result = int(a) + int(b)
    elif operator == '-':
        result = int(a) - int(b)
    elif operator == '*':
        result = int(a) * int(b)
    
    elif operator == '/':
        if int(b) == 0:
            result = 'skibidi skibidi'
            return render_template('index.html', the_result = result)
        result = int(a) / int(b)

    return render_template('index.html', the_result = result)

app.run(debug= True)