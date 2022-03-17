from KBQA.answer_search import AnswerSearcher


class QuestionTemplates:
	def __init__(self):
		self.neo_graph = AnswerSearcher()
		self.question_list = {'1': self.get_question1,
		                      '2': self.get_question2}
		self.pattern_re = {'1':'which movie is directed by (.*?)$',
		                   '2':'which movie (.*?) acted in'}

	def search_answer(self, question, question_type):
		try:
			question_func = self.question_list[question_type]
			final_result = question_func(question)
			return final_result
		except KeyError:
			raise Exception('Question Type Error, unable to classify question')

	def extract_ner(self, question_str, pattern_num):
		import re
		pattern_str = self.pattern_re[pattern_num]
		extracted_entity = re.findall(pattern_str, question_str)[0]
		return extracted_entity

	def get_question1(self, question):
		entity_person = self.extract_ner(question,'1')
		# entity_person = 'Mike Nichols'
		cypher_str = 'match (p:Person)-[r:DIRECTED]-(n:Movie) where p.name="%s" return n.title' % entity_person
		result = self.neo_graph.run_search(cypher_str, 'list')
		return ', '.join(result)

	def get_question2(self, question):
		entity_person = self.extract_ner(question,'2')
		# entity_person = 'Charlize Theron'
		cypher_str = 'match (p:Person)-[r:ACTED_IN]-(n:Movie) where p.name="%s" return n.title' % entity_person
		result = self.neo_graph.run_search(cypher_str, 'list')
		return ', '.join(result)


if __name__ == '__main__':
	t = QuestionTemplates()
	t.search_answer('which movie is directed by	Mike Nichols', '2')
