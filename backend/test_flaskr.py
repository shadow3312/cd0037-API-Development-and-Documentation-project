import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:shadow@{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        ''' Test pour confirmer l'envoi des categories effectué avec succès '''
        res = self.client().get(f'/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_405_post_categories(self):
        ''' Test pour confirmer l'envoi de la réponse appropriée en essayant d'enregistrer une catégorie '''
        res = self.client().post(f'/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Methode non autorisée')

    def test_200_get_questions_by_category(self):
        ''' Test pour confirmer l'envoi avec succès des questions en fonction d'une catégorie '''
        res = self.client().get(f'/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
    
    def test_404_get_questions_by_category(self):
        ''' Test pour confirmer l'envoi de la réponse appropriée pour l'affichage des questions dans une catégorie inexistante '''
        res = self.client().get(f'/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Ressource non trouvée')

    def test_200_get_questions(self):
        ''' Test pour confirmer l'envoi avec succes des questions '''
        res = self.client().get(f'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    def test_404_get_questions(self):
        ''' Test pour confirmer l'envoi de la réponse appropriée en essayant d'accéder à une page vide de questions '''
        res = self.client().get(f'/questions?page=1500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Ressource non trouvée')

    def test_201_post_questions(self):
        ''' Test pour confirmer l'enregistrement avec succes d'une question '''
        params = {
            "question": "Quelle est la capitale du Congo ?",
            "answer": "Brazzaville",
            "category": 3,
            "difficulty": 2
        }
        res = self.client().post(f'/questions', json=params)
        data = json.loads(res.data)
        question = Question.query.order_by(Question.id.desc()).first().format()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], question['id'])
    
    def test_422_post_questions(self):
        ''' Test pour confirmer l'envoi de la reponse adequate en envoyant des parametres invalides pour l'enregistrement d'une question '''
        params = {
            "question": "",
            "answer": "",
            "category": 0,
            "difficulty": 0
        }
        res = self.client().post(f'/questions', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'La requête ne peut pas être traitée')
    
    def test_200_search_questions(self):
        ''' Test pour confirmer la recherche d'une question '''
        params = {
            "searchTerm": "yo"
        }
        res = self.client().post(f'/questions/search', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_400_search_questions(self):
        ''' Test pour confirmer l'envoi de la reponse adequate pour une recherche vide '''
        params = {
            "searchTerm": None
        }
        res = self.client().post(f'/questions/search', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Requête invalide')

    def test_200_delete_questions(self):
        ''' Test pour confirmer la suppression d'une question '''
        question = Question.query.order_by(Question.id.desc()).first()
        to_delete = question.id

        res = self.client().delete('/questions/'+str(to_delete))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], to_delete)

    def test_404_delete_questions(self):
        ''' Test pour confirmer l'echec de la suppression d'une question inexistante '''
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Ressource non trouvée')
    
    def test_200_post_quizzes(self):
        ''' Test pour confirmer l'affichage d'un quizz '''
        quiz_category = {
            "id": 1,
            "type": "Science"
        }
        params = {
            "previous_questions": [],
            "quiz_category": quiz_category
        }
        res = self.client().post(f'/quizzes', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_post_quizzes(self):
        ''' Test pour confirmer l'envoi de la reponse adequate en cas de requete invalide '''
        params = {
            "previous_question": None,
            "quiz_category": None
        }
        res = self.client().post(f'/quizzes', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Requête invalide')

    
    




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()