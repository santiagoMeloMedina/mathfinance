from src.client.question import Question, QuestionKind, QuestionEdge
from src.client.flow.topics import projects


def start():
    main_q0 = Question(id=0, kind=QuestionKind.SELECT, content="Escoja el tema:")

    main_q0.add_edge(
        edge=QuestionEdge(target=projects.projects_q0, alias="Project Evaluation")
    )

    main_q0.ask()
