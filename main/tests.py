from django.test import TestCase, Client
from django.urls import reverse
from .models import InterviewAttempt, Resume
import json


class InterviewTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_generate_questions_and_submit(self):
		# Generate questions
		res = self.client.post(reverse('interview_api'), json.dumps({'role': 'Data Scientist', 'count': 3}), content_type='application/json')
		self.assertEqual(res.status_code, 200)
		data = res.json()
		self.assertIn('questions', data)
		self.assertIn('attempt_id', data)

		attempt_id = data['attempt_id']
		questions = data['questions']
		# Submit dummy answers
		answers = ['Answer one', 'Short', 'Another answer']
		sub = self.client.post(reverse('interview_submit_api'), json.dumps({'attempt_id': attempt_id, 'answers': answers}), content_type='application/json')
		self.assertEqual(sub.status_code, 200)
		sj = sub.json()
		self.assertIn('result', sj)
		result = sj['result']
		# Check fallback or AI result structure
		self.assertIn('scores', result)
		self.assertIn('feedback', result)
		self.assertIn('overall_score', result)


class ResumeTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_resume_save_and_json_download(self):
		# Post resume form
		payload = {
			'name': 'Test User',
			'summary': 'A short summary',
			'experiences': 'Company A - role\nCompany B - role',
			'education': 'BS Computer Science',
			'skills': 'Python, SQL'
		}
		res = self.client.post(reverse('resume'), payload)
		# After save, redirect to resume_download
		self.assertEqual(res.status_code, 302)
		# Now download
		dl = self.client.get(reverse('resume_download'))
		self.assertEqual(dl.status_code, 200)
		self.assertEqual(dl['Content-Type'], 'application/json')

	def test_resume_pdf_download(self):
		# Create resume directly
		r = Resume.objects.create(name='PDF User', data_json=json.dumps({'summary':'X','experiences':'Y','education':'Z','skills':'K'}))
		dl = self.client.get(reverse('resume_download') + '?pdf=1')
		self.assertEqual(dl.status_code, 200)
		self.assertEqual(dl['Content-Type'], 'application/pdf')

