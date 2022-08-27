import os
from urllib import response
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        # On renvoie la reponse au format {"1": "Science", "2": "Sports", "3": "History"}
        formatted_categories = {category.id: category.type for category in categories}
        response = jsonify({'categories':formatted_categories})
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        # On veut limiter la liste des questions à afficher dans le json en faisant un slice du tableau formatted_questions entre le premier element du tableau à notre position initiale et le max QUESTIONS_PER_PAGE
        # On commence par récupérer l'argument page envoyé dans l'url. Par défaut, on est sur la première page
        page = request.args.get('page', 1, type=int)
        # Par défaut le premier element du tableau sera à l'index 0, à la prochaine page ce sera l'index 10, puis l'index 20 et ainsi de suite
        start = (page - 1) * QUESTIONS_PER_PAGE
        # Pour l'autre extrémité de notre slice, on ajoute la valeur de QUESTIONS_PER_PAGE à notre index de départ
        end = start + QUESTIONS_PER_PAGE

        response = None
        # S'il n'y a aucune question sur une page donnée(e.g: ?page=500), on renvoie une erreur 404
        if len(formatted_questions[start:end]) > 0:
            response = jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': {category.id: category.type for category in Category.query.all()},
                'current_category': None
            })
        else:
            abort(404)

        return response

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        # Si aucune question n'est associée à l'id envoyée on renvoie un 404, sinon on supprime la question
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question')
        answer = body.get('answer')
        category = int(body.get('category'))
        difficulty = int(body.get('difficulty'))

        # On vérifie que les champs requis sont bien renseignés
        if question is None or answer is None or category is None or difficulty is None:
            abort(400)

        try:
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            }), 201
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term is None:
            abort(400)

        #Filtre insensible à la case
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': None
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]
        if len(formatted_questions) > 0:
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category_id
            })
        else:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')

        if previous_questions is None or category is None:
            abort(400)

        # Si l'utilise selectionne ALL, on retourne TOUTES les questions qui n'ont pas déjà été posées, sinon on filtre par la catégorie sélectionnée
        if category['id'] == 0:
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.filter(Question.category == category['id']).filter(Question.id.notin_(previous_questions)).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            # On ne retourne un résultat que si les questions ne sont pas vides, sinon on ne renvoie rien
            'question': formatted_questions[0] if len(formatted_questions) > 0 else None
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Requête invalide"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Ressource non trouvée"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Methode non autorisée"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "La requête ne peut pas être traitée"
        }), 422


    if __name__ =='__main__':
        app.debug=True
        app.run(host='0.0.0.0', port=5000)

    return app

