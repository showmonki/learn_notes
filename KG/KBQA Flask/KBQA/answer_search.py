from py2neo import Graph


class AnswerSearcher:
	def __init__(self):
		self.g = Graph(
			"bolt://localhost:7687", auth=('neo4j','123456')
		)

	def run_search(self, cypher_str,result_type=None):
		if result_type == 'list':
			result = list(self.g.run(cypher_str).to_series())
		else:
			result = self.g.run(cypher_str)
		return result
