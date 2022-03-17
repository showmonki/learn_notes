from KBQA.question_templates import QuestionTemplates
from KBQA.question_clf import QuestionClf


class KBQAChat:
	def __init__(self):
		self.clf = QuestionClf()
		self.question_temp = QuestionTemplates()

	def get_answer(self, question):
		question_type = self.clf.predict(question)
		try:
			answer = self.question_temp.search_answer(question, question_type)
		except Exception:
			answer = 'Warning: 无答案，需优化'
		return answer

	def get_feedback(self, feedback):
		""" feedback about answer from user for improvements"""
		self.feedback = feedback