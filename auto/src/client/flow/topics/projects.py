from src.client.question import Question, QuestionKind, QuestionEdge


projects_q0 = Question(id=0, kind=QuestionKind.SELECT, content="Que desea hacer?")
projects_q1 = Question(
    id=1, kind=QuestionKind.INPUT, content=("id", "Indique ID del proyecto:", str)
)
projects_q2 = Question(
    id=2, kind=QuestionKind.SELECT, content="Que desea hacer en el proyecto?"
)
projects_q3 = Question(
    id=3, kind=QuestionKind.INPUT, content=("amount", "Escriba el monto $:", float)
)
projects_q4 = Question(
    id=4,
    kind=QuestionKind.INPUT,
    content=[("quantity", "Cantidad:", int), ("amount", "Monto $:", float)],
)


projects_q0.add_edge(edge=QuestionEdge(target=projects_q1, alias="Agregar proyecto"))

projects_q1.add_edge(edge=QuestionEdge(target=projects_q2))

projects_q2.add_edge(edge=QuestionEdge(target=projects_q3, alias="Agregar monto"))
projects_q2.add_edge(
    edge=QuestionEdge(target=projects_q4, alias="Agregar multiples montos iguales")
)
projects_q2.add_edge(edge=QuestionEdge(target=projects_q0, alias="Confirmar"))

projects_q3.add_edge(edge=QuestionEdge(target=projects_q2))

projects_q4.add_edge(edge=QuestionEdge(target=projects_q2))
