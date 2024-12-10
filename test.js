const string = ```json
[
  {"questionID": "Q1-1", "answer": "A", "question": "This is question 1 of quiz 1.", "max_score": 10, "modelEval": 0},
  {"questionID": "Q1-2", "answer": "A", "question": "This is question 2 of quiz 1.", "max_score": 17, "modelEval": 100},
  {"questionID": "Q1-3", "answer": "C", "question": "This is question 3 of quiz 1.", "max_score": 10, "modelEval": 0},
  {"questionID": "Q1-4", "answer": "B", "question": "This is question 4 of quiz 1.", "max_score": 16, "modelEval": 100},
  {"questionID": "Q1-5", "answer": "D", "question": "This is question 5 of quiz 1.", "max_score": 13, "modelEval": 0},
  {"questionID": "Q2-1", "answer": "C", "question": "This is question 1 of quiz 2.", "max_score": 11, "modelEval": 0},
  {"questionID": "Q2-2", "answer": "C", "question": "This is question 2 of quiz 2.", "max_score": 18, "modelEval": 100},
  {"questionID": "Q2-3", "answer": "B", "question": "This is question 3 of quiz 2.", "max_score": 13, "modelEval": 0},
  {"questionID": "Q2-4", "answer": "C", "question": "This is question 4 of quiz 2.", "max_score": 16, "modelEval": 100},
  {"questionID": "Q2-5", "answer": "B", "question": "This is question 5 of quiz 2.", "max_score": 15, "modelEval": 0},
  {"questionID": "Q3-1", "answer": "A", "question": "This is question 1 of quiz 3.", "max_score": 20, "modelEval": 100},
  {"questionID": "Q3-2", "answer": "C", "question": "This is question 2 of quiz 3.", "max_score": 7, "modelEval": 0},
  {"questionID": "Q3-3", "answer": "A", "question": "This is question 3 of quiz 3.", "max_score": 15, "modelEval": 100},
  {"questionID": "Q3-4", "answer": "C", "question": "This is question 4 of quiz 3.", "max_score": 8, "modelEval": 0},
  {"questionID": "Q3-5", "answer": "B", "question": "This is question 5 of quiz 3.", "max_score": 15, "modelEval": 100}
]
```

const reponse = JSON.parse(string)

console.log(reponse)