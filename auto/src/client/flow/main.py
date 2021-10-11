from src.client import console


MAIN_QUESTIONS = "Which topic is the problem on?"
TOPICS = {
    "Linear Gradient": lambda: print("lg"),
    "Geometric Gradient": lambda: print("gg"),
    "Project Evaluation": lambda: print("pe"),
}


def go_to_section(option: str):
    return TOPICS[option]()


def start():
    console.Console.print_options(
        question=MAIN_QUESTIONS, options=list(TOPICS.keys()), action=go_to_section
    )
