from flask import Flask, render_template, request, redirect, url_for, session
import asyncio
from video_processing import load_transcript, split_transcript
from chat_model import get_response_from_query
from database import create_db, search_similar_documents

app = Flask(__name__)
app.secret_key = "280404"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        return redirect(url_for('chat', video_url=video_url))
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    video_url = request.args.get('video_url')
    transcript = asyncio.run(load_transcript(video_url))
    docs = split_transcript(transcript)
    db = create_db(docs)

    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        user_question = request.form['user_question']
        similar_docs = search_similar_documents(db, user_question)
        response = get_response_from_query(user_question, similar_docs)
        session['conversation'].append({"question": user_question, "response": response})
        session.modified = True
    return render_template('chat.html', video_url=video_url, conversation=session['conversation'])

@app.route('/clear_history')
def clear_history():
    session.pop('conversation', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
