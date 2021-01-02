import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import os


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')  

        self.database_path = "postgresql://{}:{}@{}/{}".format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What is the largest country?',
            'answer': 'Russia',
            'category': 3,
            'difficulty': 2
        }

        self.search_term = 'tom'

        self.previous_questions = []
        
        self.quiz_category = {
            'id': 2,
            'type': 'Art'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_get_all_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')


    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])


    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')


    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_404_create_new_question(self):
        res = self.client().post('/questions/', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')


    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(question, None)


    def test_422_delete_question(self):
        res = self.client().delete('/questions/150')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity!')

    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], 2)


    def test_404_get_category_questions(self):
        res = self.client().get('/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')


    def test_search_for_question(self):
        res = self.client().post('/search_questions', json={'searchTerm': self.search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_404_search_for_question(self):
        res = self.client().post('/search_questions/', json={'searchTerm': self.search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

    
    def test_take_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': self.previous_questions, 'quiz_category': self.quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_404_take_quiz(self):
        res = self.client().post('/quizzes/', json={'previous_questions': self.previous_questions, 'quiz_category': self.quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()