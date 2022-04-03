import os
import sys
from src.client.question import Question, QuestionKind, QuestionEdge
from src.client.flow.topics import (
    projects,
    mutually,
    linear_gradient,
    geometric_gradient, 
    rate
)


class Graph:
    def __init__(self):
        self.main = Question(
            kind=QuestionKind.SELECT,
            content="Escoja el tema:",
        )
        project = Question(kind=QuestionKind.FINAL, process=self.__project_evaluation)
        l_gradient = Question(kind=QuestionKind.FINAL, process=self.__linear_gradient)
        g_gradient = Question(
            kind=QuestionKind.FINAL, process=self.__geometric_gradient
        )
        calculate_rate = Question(
            kind=QuestionKind.FINAL, process=self.__calculate_rate
        )
        off = Question(kind=QuestionKind.FINAL, process=self.__exit)

        self.main.add_edge(target=project, alias="Evaluacion de Proyectos")
        self.main.add_edge(target=l_gradient, alias="Gradiente Linear")
        self.main.add_edge(target=g_gradient, alias="Gradiente Geometrico")
        self.main.add_edge(target=calculate_rate, alias="Calcular tasa")
        self.main.add_edge(target=off, alias="Salir")

        self.main.ask()
    
    def __calculate_rate(self):
        rate.FormRateTopic(last_state=self.main)

    def __project_evaluation(self):
        mutually.FormMutually(last_state=self.main)

    def __linear_gradient(self):
        linear_gradient.FormLinearGradient(last_state=self.main)

    def __geometric_gradient(self):
        geometric_gradient.FormGeometricGradient(last_state=self.main)

    def __exit(self):
        os.system("clear")
        sys.exit()
