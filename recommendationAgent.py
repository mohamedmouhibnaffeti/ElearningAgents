import psycopg2
from psycopg2.extras import DictCursor
import ollama
import ast
import pickle
from supabase import create_client, Client
import os

url: str = "https://uhwjxhfreuaqitwkoblg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVod2p4aGZyZXVhcWl0d2tvYmxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEzMTI3NDUsImV4cCI6MjA0Njg4ODc0NX0.6XmU5VIwQEkhyPAannMjsYGJlt50shC0BqLvO1b5nC8"
supabase: Client = create_client(url, key)

def getAllUsers():
    print(url, key)
    response = supabase.table('User').select().execute()
    return response.data

# Function to get user info by user_id
def get_user_info(user_id):
    response = supabase.table('User').select('*').eq('id', user_id).single().execute()
    if(not response.data):
        return {}
    return response.data

# Function to get filtered courses based on preferred languages and categories
def get_filtered_courses(preferred_languages, preferred_categories, courses):
    # Filter courses based on the given languages and categories
    filtered_courses = [
        course for course in courses
        if (not preferred_languages or course['language'] in preferred_languages) and
           (not preferred_categories or course['category'] in preferred_categories)
    ]
    
    return filtered_courses



# Function to get all courses
def get_all_courses():
    response = supabase.table('Course').select('*').execute()
    return response.data














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
import pickle

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




courses = get_all_courses()
print(courses)

def update_Q_value(course_id, feedback, user_id):
    state_action = (user_id, course_id)

    # If Q-value for this state-action pair is not initialized, set it to 0
    if state_action not in Q_table:
        Q_table[state_action] = 0

    # Calculate the updated Q-value
    old_value = Q_table[state_action]
    reward = feedback  # Treat feedback as the reward
    best_future_q = max(Q_table.get((user_id, c["id"]), 0) for c in get_all_courses())
    new_value = old_value + learning_rate * (reward + discount_factor * best_future_q - old_value)

    # Update Q-table with the new Q-value
    Q_table[state_action] = new_value
    print(f"Updated Q-value for user {user_id} and course {course_id}: {Q_table[state_action]}")
    save_q_table("Recommendation_Q_table.pkl")



def llama_recommendation(user_id):
    load_q_table("Recommendation_Q_table.pkl")

    user_info = get_user_info(user_id)
    preferred_languages = user_info.get("preferredLanguages", [])
    preferred_categories = user_info.get("preferredCategories", [])


    filtered_courses= get_filtered_courses(preferred_languages, ["Web Development", "Machine Learning"], courses)
    if(len(filtered_courses) == 0):
        return []
    print(filtered_courses)
    filtered_data = {key: value for key, value in Q_table.items() if key[0] == user_id}


    prompt = (
        f"Based on the user profile: {user_info} and provided Q-values: {filtered_data}, "
        f"select ideal courses from the course list: {filtered_courses}, and don't include any other courses outside the list."
        "Provide recommendations in the following format by only including the course ids in an array of strings: "
        "[courseid1, courseid2, courseid3, ...] "
        "with no additional text, explanations, or formatting."
    )




    # Generate recommendations using LLaMA
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    if(response.get("error")):
        return []
    recommended_content = response["message"]["content"].strip()
    if(not recommended_content):
        return []
    print(recommended_content)
    try:
        recommendations = ast.literal_eval(recommended_content)
    except (ValueError, SyntaxError) as e:
        print(e)
        return {"error": f"Failed to parse recommendation: {e}"}

    return recommendations




