from flask import Flask, render_template, request
import os
import json
import random

app = Flask(__name__)

# Path to chapters folder
CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), 'chapters')
chapters = {f.replace('.json', ''): os.path.join(CHAPTERS_DIR, f) 
            for f in os.listdir(CHAPTERS_DIR) if f.endswith('.json')}

def load_questions(selected_chapters):
    combined_questions = {"section_a": [], "section_b": [], "section_c": [], "section_d": []}
    
    for chapter in selected_chapters:
        path = chapters.get(chapter)
        if path:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for section in combined_questions.keys():
                    if section in data:
                        combined_questions[section].extend(data[section])
    
    return combined_questions

@app.route('/', methods=['GET', 'POST'])
def index():
    question_paper = None
    selected_chapters = []
    num_questions = {"section_a": 0, "section_b": 0, "section_c": 0, "section_d": 0}

    if request.method == 'POST':
        selected_chapters = request.form.getlist('chapters')
        num_questions = {
            "section_a": int(request.form.get('section_a') or 0),
            "section_b": int(request.form.get('section_b') or 0),
            "section_c": int(request.form.get('section_c') or 0),
            "section_d": int(request.form.get('section_d') or 0)
        }

        all_questions = load_questions(selected_chapters)
        
        question_paper = {}
        for section, count in num_questions.items():
            if count > 0 and len(all_questions[section]) > 0:
                question_paper[section] = random.sample(all_questions[section], min(count, len(all_questions[section])))

    return render_template('index.html', chapters=chapters.keys(), paper=question_paper)

if __name__ == '__main__':
    app.run(debug=True)
