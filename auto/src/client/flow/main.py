import os
from src.client.question import Question, QuestionKind, QuestionEdge
from src.client.flow.topics import projects, mutually, linear_gradient


class Graph:
    def __init__(self):
        self.main = Question(
            kind=QuestionKind.SELECT,
            content="Escoja el tema:",
        )
        project = Question(kind=QuestionKind.FINAL, process=self.__project_evaluation)
        linear_gradient = Question(
            kind=QuestionKind.FINAL, process=self.__linear_gradient
        )
        off = Question(kind=QuestionKind.FINAL, process=self.__exit)

        self.main.add_edge(target=project, alias="Evaluacion de Proyectos")
        self.main.add_edge(target=linear_gradient, alias="Gradientes Lineares")
        self.main.add_edge(target=off, alias="Salir")

        self.main.ask()

    def __project_evaluation(self):
        mutually.FormMutually(last_state=self.main)

    def __linear_gradient(self):
        linear_gradient.FormLinearGradient(last_state=self.main)

    def __exit(self):
        os.system("clear")
        exit()
