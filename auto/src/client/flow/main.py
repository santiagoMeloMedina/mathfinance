import os
from src.client.question import Question, QuestionKind, QuestionEdge
from src.client.flow.topics import projects, mutually


class Graph:
    def __init__(self):
        self.main = Question(
            kind=QuestionKind.SELECT,
            content="Escoja el tema:",
        )
        project = Question(kind=QuestionKind.FINAL, process=self.__project_evaluation)
        off = Question(kind=QuestionKind.FINAL, process=self.__exit)

        self.main.add_edge(
            edge=QuestionEdge(target=project, alias="Evaluacion de Proyectos")
        )
        self.main.add_edge(edge=QuestionEdge(target=off, alias="Salir"))

        self.main.ask()

    def __project_evaluation(self):
        mutually.FormMutually(last_state=self.main)

    def __exit(self):
        os.system("clear")
        exit()
