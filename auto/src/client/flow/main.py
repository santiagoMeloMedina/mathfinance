from src.client.question import Question, QuestionKind, QuestionEdge
from src.client.flow.topics import projects, mutually


def start():
    main_q0 = Question(kind=QuestionKind.SELECT, content="Escoja el tema:")
    last = Question(kind=QuestionKind.FINAL)

    mutual = mutually.FormMutually(last_state=last)
    print(mutual.__dict__)
