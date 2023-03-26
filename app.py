import openai
from flask import Flask, render_template, request

app = Flask(__name__)

openai.api_key = "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"
engine = "text-davinci-003"
temperature = 0.6
max_tokens = 150
chat_history = []

def askGPT(text):
    response = openai.Completion.create(
        engine=engine,
        prompt=text,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        if len(chat_history) % 2 == 0:
            chat_history.append("Human: " + question)
            answer = askGPT("Human: " + question + "\nAI: ")
            chat_history.append("AI: " + answer)
        else:
            chat_history.append("AI: " + question)
            answer = askGPT("Human: " + chat_history[-2] + "\nAI: " + question + "\nAI: ")
            chat_history.append("Human: " + answer)
        return render_template('templates/index.html', chat_history=chat_history)
    else:
        return render_template('templates/index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
