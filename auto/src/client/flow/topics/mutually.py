from typing import List
from src.client.flow.topics import projects
from src.client.flow.topics import form as topic_form
from src.client.question import Question, QuestionKind
from src.metrics.bussiness import Index, MutuallyEsclusive, Project


class FormMutually(topic_form.Form):
    def __init__(self, last_state: Question):
        super().__init__(title="Que deseas hacer?", last=last_state, back_title="Atras")

        self.projects: List[Project] = []
        self.budget = 0

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

        self.bidirect(target=add_pro, alias="Agregar proyecto")
        self.bidirect(target=del_pro, alias="Borrar proyecto")
        self.bidirect(target=set_budget, alias="Configurar presupuesto")

        self.direct(target=show_pro, alias="Ver proyecto")
        self.direct(target=show_rank, alias="Ver ranking")
        self.direct(target=show_rank_budget, alias="Ver ranking con presupuesto")

        self.run_form()

    def add_project(self):
        project = projects.FormProject(
            last_state=Question(kind=QuestionKind.FINAL)
        ).project
        self.projects.append(project)
        self.run_form()

    def delete_project(self, id: str):
        tmp = list(filter(lambda x: x.id is not id, self.projects))
        self.projects = tmp

    def set_budget(self, value: float):
        self.budget = value

    def show_project(self):
        temp = Question(kind=QuestionKind.SELECT, content="Escoja el proyecto:")
        temp.add_edge(target=self.main, alias="Atras")
        for project in self.projects:
            tmp = Question(
                kind=QuestionKind.SELECT,
                content=f"Project {project.id}\n{str(Index(project=project))}",
            )
            temp.add_edge(target=tmp, alias=f"Project {project.id}")
            tmp.add_edge(target=temp, alias="Atras")

        temp.ask()

    def show_ranking(self):
        mutually_esclusive = MutuallyEsclusive(projects=self.projects)
        temp = Question(
            kind=QuestionKind.SELECT,
            content=f"Ranking de proyectos\n{mutually_esclusive.str_ranking()}",
        )
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def show_rank_by_budget(self):
        mutually_esclusive = MutuallyEsclusive(projects=self.projects)
        temp = Question(
            kind=QuestionKind.SELECT,
            content=f"Ranking de proyectos\n{mutually_esclusive.budget_rank(self.budget)}",
        )
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()
