from typing import List
from src.client.flow.topics import projects
from src.client.question import Question, QuestionKind, QuestionEdge
from src.metrics.bussiness import Index, MutuallyEsclusive, Project


class FormMutually:
    def __init__(self, last_state: Question):

        self.projects: List[Project] = []
        self.budget = 0

        self.main = Question(kind=QuestionKind.SELECT, content="Que deseas hacer?")

        add_pro = Question(kind=QuestionKind.FINAL, process=self.add_project)
        del_pro = Question(
            kind=QuestionKind.INPUT,
            content=("id", "ID:", str),
            process=self.delete_project,
        )
        set_budget = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Presupuesto:", float),
            process=self.set_budget,
        )
        show_pro = Question(kind=QuestionKind.FINAL, process=self.show_project)
        show_rank = Question(kind=QuestionKind.FINAL, process=self.show_ranking)
        show_rank_budget = Question(
            kind=QuestionKind.FINAL, process=self.show_rank_by_budget
        )
        back = Question(kind=QuestionKind.LINK)

        self.main.add_edge(edge=QuestionEdge(target=add_pro, alias="Agregar proyecto"))
        self.main.add_edge(edge=QuestionEdge(target=del_pro, alias="Borrar proyecto"))
        self.main.add_edge(
            edge=QuestionEdge(target=set_budget, alias="Configurar presupuesto")
        )
        self.main.add_edge(edge=QuestionEdge(target=show_pro, alias="Ver proyecto"))
        self.main.add_edge(edge=QuestionEdge(target=show_rank, alias="Ver ranking"))
        self.main.add_edge(
            edge=QuestionEdge(
                target=show_rank_budget, alias="Ver ranking con presupuesto"
            )
        )
        self.main.add_edge(edge=QuestionEdge(target=back, alias="Atras"))

        add_pro.add_edge(edge=QuestionEdge(target=self.main))
        del_pro.add_edge(edge=QuestionEdge(target=self.main))
        set_budget.add_edge(edge=QuestionEdge(target=self.main))

        back.add_edge(edge=QuestionEdge(target=last_state))

        self.main.ask()

    def add_project(self):
        project = projects.FormProject(
            last_state=Question(kind=QuestionKind.FINAL)
        ).project
        self.projects.append(project)
        self.main.ask()

    def delete_project(self, id: str):
        tmp = list(filter(lambda x: x.id is not id, self.projects))
        self.projects = tmp

    def set_budget(self, value: float):
        self.budget = value

    def show_project(self):
        temp = Question(kind=QuestionKind.SELECT, content="Escoja el proyecto:")
        temp.add_edge(edge=QuestionEdge(target=self.main, alias="Atras"))
        for project in self.projects:
            tmp = Question(
                kind=QuestionKind.SELECT,
                content=f"Project {project.id}\n{str(Index(project=project))}",
            )
            temp.add_edge(edge=QuestionEdge(target=tmp, alias=f"Project {project.id}"))
            tmp.add_edge(edge=QuestionEdge(target=temp, alias="Atras"))

        temp.ask()

    def show_ranking(self):
        mutually_esclusive = MutuallyEsclusive(projects=self.projects)
        temp = Question(
            kind=QuestionKind.SELECT,
            content=f"Ranking de proyectos\n{mutually_esclusive.str_ranking()}",
        )
        temp.add_edge(edge=QuestionEdge(target=self.main, alias="Atras"))
        temp.ask()

    def show_rank_by_budget(self):
        mutually_esclusive = MutuallyEsclusive(projects=self.projects)
        temp = Question(
            kind=QuestionKind.SELECT,
            content=f"Ranking de proyectos\n{mutually_esclusive.budget_rank(self.budget)}",
        )
        temp.add_edge(edge=QuestionEdge(target=self.main, alias="Atras"))
        temp.ask()
