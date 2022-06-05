import sys
from settings.initialization import initialize_abstraction
from project_management.abstractor import execute_program

sys.path.append(".")


def execute_abstractor():
    abstract = initialize_abstraction()
    execute_program(abstract)
    abstract.stop_program_timer()
    quit()


execute_abstractor()
