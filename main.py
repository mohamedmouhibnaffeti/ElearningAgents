from EvaluationAgent import llama_evaluation, update_evaluation_Q_table
from flask import Flask, render_template, jsonify, request
from recommendationAgent import *
from AssessmentAgent import *





app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    users = getAllUsers()
    return jsonify(users) 

#----------------RecommendationAgent----------------#

@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    user_id = request.json.get("user_id")
    recommendations = llama_recommendation(user_id)
    print(recommendations)
    return jsonify(recommendations)



@app.route('/recommendationfeedback', methods=['POST'])
def update_feedback():
    user_id = request.json.get("user_id")
    course_id = request.json.get("course_id")
    feedback = request.json.get("feedback")

    if feedback not in [-1, 0, 1]:
        return jsonify({"error": "Invalid feedback value. Must be -1, 0, or 1."})

    update_Q_value(course_id, feedback, user_id)

    return jsonify({"message": "Feedback updated successfully."})







#----------------AssessmentAgent----------------#


@app.route('/Assessment', methods=['POST'])
def assess_user():
    user_id = request.json.get("user_id")
    print(user_id)
    assessment = llama_assessment(user_id)
    return jsonify({"assessment": assessment})



@app.route('/Assessmentfeedback', methods=['POST'])
def feedback():
    user_id = request.json.get('user_id')
    assessment = request.json.get('assessment')
    feedback_value = request.json.get('feedback')

    
    # Update Q-value based on feedback
    update_Q_value(assessment, feedback_value, user_id)
    
    return jsonify({"status": "Feedback received and Q-value updated!"})


#----------------EvaluationAgent----------------#


@app.route('/Evaluation', methods=['POST'])
def evaluation_user():
    quizid = request.json.get("quizid")
    responses = request.json.get("responses")
    print(responses)
    evaluation = llama_evaluation(quizid, responses)
    """quiz_id = request.json.get('quiz_id')
    teacher_id = request.json.get('teacher_id')
    answers = request.json.get('answers')
    evaluation = llama_evaluation(quiz_id, answers)
    
    
    insert_evaluation(teacher_id, quiz_id, evaluation)"""
    print(evaluation)

    return jsonify({"evaluation": evaluation})



@app.route('/Evaluationfeedback', methods=['POST'])
def evaluation_feedback():
    quiz_id = request.json.get('quiz_id')
    evaluation = request.json.get('evaluation')
    feedback = request.json.get('feedback')

    update_evaluation_Q_table(evaluation, feedback, quiz_id)
    
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)