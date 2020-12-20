import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    # CORS Headers
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def current_category():
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}
        return formatted_categories

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format()
                               for question in selection]
        current_questions = formatted_questions[start:end]

        return current_questions
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = {
                category.id: category.type for category in categories}
            return jsonify({
                'success': True,
                'categories': formatted_categories
            })
        except:
            abort(404)

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:

            selection = Question.query.order_by(Question.id).all()
            formatted_questions = paginate_questions(request, selection)
            current_cat = current_category()

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(selection),
                'categories': current_cat
            })
        except:
            abort(404)
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'deleted': q_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:

            body = request.get_json()

            new_question = body.get('question', None)
            if new_question is None:
                abort(400)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)
            new_answer = body.get('answer', None)

            question = Question(question=new_question, category=new_category,
                                difficulty=new_difficulty, answer=new_answer)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
                'question': question.question,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()

            search_term = body.get('searchTerm', None)

            form = "%{}%".format(search_term)
            selection = Question.query.filter(
                Question.question.ilike(form)).all()
            formatted_questions = paginate_questions(request, selection)
            current_cat = current_category()

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(selection),
                'categories': current_cat
            })
        except:
            abort(404)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def get_by_category(cat_id):
        try:
            selection = Question.query.filter(
                Question.category == cat_id).all()
            formatted_questions = paginate_questions(request, selection)

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'current_category': selection[0].category,
                'questions': formatted_questions,
                'total_questions': len(selection)
            })

        except:
            abort(404)

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        try:
            random
            body = request.get_json()

            quiz_category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if quiz_category['id'] == 0:
                selection = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                selection = Question.query.filter(
                    Question.category == quiz_category['id'], Question.id.notin_(previous_questions)).all()

            formatted_questions = paginate_questions(request, selection)

            current_category = 0
            if len(formatted_questions) == 0:
                formatted_questions = ''
            else:
                formatted_questions = random.choice(formatted_questions)
                current_category = selection[0].category

            return jsonify({
                'success': True,
                'current_category': current_category,
                'question': formatted_questions,
                'total_questions': len(selection)
            })
        except:
            abort(400)
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
    return app
