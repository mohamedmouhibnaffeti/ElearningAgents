import pickle
from flask import Flask, render_template, jsonify, request
import ollama
import psycopg2



# Q-learning parameters
learning_rate = 0.1       # Determines how much new information overrides the old
discount_factor = 0.9     # Value placed on future rewards
epsilon = 0.2             # Probability of choosing exploration over exploitation

# Initialize a Q-table as a dictionary where keys are (user_id, course_id) pairs, values are Q-values
Q_table = {}

# Function to save the Q-table to a file
def save_q_table(filename):
    with open(f'tables/{filename}', "wb") as f:
        pickle.dump(Q_table, f)
    print("Q-table saved to", f'tables/{filename}')




# Function to load the Q-table from a file
def load_q_table(filename):
    global Q_table
    try:
        with open(f'tables/{filename}', "rb") as f:
            Q_table = pickle.load(f)
        print("Q-table loaded from", f'tables/{filename}')
    except FileNotFoundError:
        print("No Q-table found. Creating a new Q-table.")
        Q_table = {}
        # Save the new Q-table to the specified file
        with open(f'tables/{filename}', "wb") as f:
            pickle.dump(Q_table, f)
        print("New Q-table created and saved to", f'tables/{filename}')






def update_evaluation_Q_table(evaluation, feedback, quiz_id):
    state_action = (quiz_id, evaluation)
    
    # Initialize Q-value if not present
    if state_action not in Q_table:
        Q_table[state_action] = 0
    
    # Retrieve the old Q-value
    old_value = Q_table[state_action]
    reward = feedback  # Feedback is treated as the reward
    
    # Get the best Q-value for future states
    future_q_values = [Q_table.get((quiz_id, next_action), 0) for next_action in Q_table]
    best_future_q = max(future_q_values) if future_q_values else 0  # Use 0 if no future Q-values exist
    
    # Calculate the updated Q-value
    new_value = old_value + learning_rate * (reward + discount_factor * best_future_q - old_value)
    
    # Update the Q-table with the new Q-value
    Q_table[state_action] = new_value
    print(f"Updated Q-value for user {quiz_id} and evaluation {evaluation}: {Q_table[state_action]}")
    save_q_table("evaluation_Q_table.pkl")








def llama_evaluation(quiz_id, answers):
    load_q_table("Evaluation_Q_table.pkl")
    filtered_data = {key: value for key, value in Q_table.items() if key[0] == quiz_id}

    prompt = (
        f"Given the data: {answers} and the provided Q-values table: {filtered_data}, "
        "add an attribute 'modelEval' to each instance in the data to represent the evaluation of the 'answer' compared to the 'question' and 'actualAnswer' attributes. "
        "Ensure that 'modelEval' does not exceed the 'max_score' for each instance ad it should be a number. "
        "Output only the valid JSON array in this format and this format only: "
        "[{'questionID': questionID, 'answer': answer, 'question': question, 'max_score': max_score, 'modelEval': modelEval}]. "
        "Respond strictly with a valid JSON array and do not include any explanation, text, or code around it."
    )



        

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()
        















































































"""
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def quiz():
    result = None
    quiz_with_indices = list(enumerate(python_quiz_with_scores))  # Generate list with index
    if request.method == 'POST':
        # Get the answers from the form
        answers = {}
        for i, question in enumerate(python_quiz_with_scores):
            answer = request.form.get(f'question_{i}')
            answers[f'question_{i}'] = answer

        # Evaluate the answers and calculate score
        result = llama_evaluation(python_quiz_with_scores, answers)
    
    return render_template('quiz.html', quiz=quiz_with_indices, result=result)


def calculate_score(quiz, answers):
    score = 0
    for i, question in enumerate(quiz):
        correct_answer = question['answer']
        user_answer = answers.get(f'question_{i}')
        if user_answer == correct_answer:
            score += question['score']
    return score


if __name__ == '__main__':
    app.run(debug=True)
"""





