import pytest
from KBQA.question_templates import QuestionTemplates


def test_question1():
	t = QuestionTemplates()
	answer = t.search_answer('which movie is directed by Mike Nichols', '1')
	assert answer == "The Birdcage, Charlie Wilson's War"


def test_question2():
	t = QuestionTemplates()
	answer = t.search_answer('which movie Charlize Theron acted in', '2')
	assert answer == "That Thing You Do, The Devil's Advocate"


def test_question_not_existed():
	t = QuestionTemplates()
	with pytest.raises(Exception) as e:
		t.search_answer('which movie is directed by	Mike Nichols', '999')
	assert e.type == Exception
	assert e.value.__str__() == 'Question Type Error, unable to classify question'



if __name__ == '__main__':
	pytest.main()