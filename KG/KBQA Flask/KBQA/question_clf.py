"""
规则匹配+NLP文本分类
"""

class QuestionClf:
	def __init__(self):
		pass

	def predict(self,question):
		question_num = self.rule_match(question)
		return question_num

	def rule_match(self,question):
		import re
		question_lower =  question.lower()
		pattern_list = {'directed by':'1','acted in':'2'}
		for str_pattern, group_num in pattern_list.items():
			if re.search(str_pattern,question_lower):
				return group_num
		else:
			pass

	def nlp_predict(self,question):
		pass