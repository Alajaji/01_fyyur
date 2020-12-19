# Trivia API
This is a tirivia api app

# APIs
## Catagories APIs
# get_categories: 
GET requests for all available categories.

# Method URI
```bash
Get /categories
```

# Response
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
# get_by_category: 
GET requests for questions based on category.

# Method URI
```bash
Get /categories/<int:cat_id>/questions
```

# Response
```bash
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "me",
            "category": 1,
            "difficulty": 5,
            "id": 29,
            "question": "hi"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

## Questions APIs
# get_questions: 
GET requests for all available questions.

# Method URI
```bash
Get /questions
```

# Response
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }...
    ],
    "success": true,
    "total_questions": 24
}
```

# delete_question: 
DELETE question using a question ID.

# Method URI
```bash
DELETE /questions/<int:q_id>
```

# Response
```bash
{
    "success": true,
    "total_questions": 24
}
```

# create_question: 
POST a new question.

# Method URI
```bash
POST /questions
```
# Request
```bash
{
    "question": "test?",
    "answer": "yes",
    "category": 2,
    "difficulty": 5
}
```
# Response
```bash
{
    "created": 32,
    "question": "test?",
    "success": true,
    "total_questions": 24
}
```

# search_question: 
POST based on a search term.

# Method URI
```bash
POST /questions/search
```
# Request
```bash
{
    "searchTerm": "cup"
}
```
# Response
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```
# APIs
## Quiz APIs
# create_quiz: 
POST to get questions to play the quiz.

# Method URI
```bash
POST /quizzes
```

# Request
```bash
{
    "previous_questions": [],
    "quiz_category": {
        "type": "click",
        "id": 1
    }
}
```
# Response
```bash
{
    "current_category": 1,
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true,
    "total_questions": 4
}
```
