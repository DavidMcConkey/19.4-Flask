from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = 'apples'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = 'responses'

@app.route('/')
def home_page():
    """Chooses a survey"""
    return render_template('home.html', survey = survey)

@app.route('/start',methods=['POST'])
def start_survey():
    """Clears responses from session"""
    session[RESPONSES] = []

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def question_handler():
    """Stores response and redirects to next question"""
    choice = request.form['answer']

    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/finish')
    else:
        return redirect(f'/questions/{len(responses)}')



@app.route('/questions/<int:id>')
def show_question(id):
    """Shows current question"""

    responses = session.get(RESPONSES)

    if(responses is None):
        #attemping to access questions out of order
        return redirect('/')
    if (len(responses) != id):
        #Attempting questions out of order
        flash(f"Wrong Question Id: {id}.")
        return redirect(f"/questions/{len(responses)}")
    if (len(responses) == len(survey.questions)):
        #Answered all the questions, thank user
        return redirect('/finish')
    
    question = survey.questions[id]
    return render_template('question.html', question_num=id,question=question)

@app.route('/finish')
def finish():
    """With completion of survey, display finish page"""
    return render_template("finish.html")
