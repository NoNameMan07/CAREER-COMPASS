from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Profile(models.Model):
	"""Simple user profile stored without auth (demo mode)."""
	name = models.CharField(max_length=120)
	email = models.EmailField(blank=True)
	location = models.CharField(max_length=120, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Conversation(models.Model):
	"""Stores a chat conversation (lightweight)."""
	title = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title or f"Conversation {self.pk}"


class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
	role = models.CharField(max_length=10, choices=(('user','user'),('assistant','assistant')))
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.role}: {self.text[:40]}"


class Recommendation(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recommendations')
	recommended_roles = models.TextField(help_text='Comma separated roles')
	created_at = models.DateTimeField(auto_now_add=True)

	def get_roles(self):
		return [r.strip() for r in self.recommended_roles.split(',') if r.strip()]


class InterviewAttempt(models.Model):
	role = models.CharField(max_length=120)
	questions = models.TextField(help_text='JSON list string of questions')
	answers = models.TextField(blank=True, help_text='JSON list string of user answers')
	score = models.FloatField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Interview {self.role} ({self.pk})"


class Resume(models.Model):
	name = models.CharField(max_length=120)
	data_json = models.TextField(help_text='JSON string of resume data')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Resume {self.name} ({self.pk})"


class CoverLetter(models.Model):
	name = models.CharField(max_length=120)
	role = models.CharField(max_length=120)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"CoverLetter {self.name} for {self.role} ({self.pk})"
