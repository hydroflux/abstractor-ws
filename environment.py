"""
This module serves as the entry point for the Abstractor application.
It initializes the abstraction process and executes the main program.

Functions:
    - execute_abstractor() -> None:
        -- Initializes the abstraction process, executes the main program, and stops the program timer.

Imports:
    - Standard Library:
        - import sys: For appending the system path and quitting the program.
    - Local:
        - from settings.initialization: For initializing the abstraction process.
        - from project_management.abstractor: For executing the main program.

Usage:
    This script is designed to be run as the main entry point for the Abstractor application.
    It initializes the necessary components and starts the main program execution.
"""

# Standard Library Import(s)
import sys

# Local Import(s)
from settings.initialization import initialize_abstraction
from project_management.abstractor import execute_program

# Add the current directory to the system path
sys.path.append(".")

def execute_abstractor() -> None:
    """
    Initializes the abstraction process, executes the main program, and stops the program timer.

    This function initializes the abstraction process by calling `initialize_abstraction()`,
    executes the main program by calling `execute_program(abstract)`, and stops the program timer
    by calling `abstract.stop_program_timer()`, which is started when the abstract is initialized.
    Finally, it quits the program.
    """
    abstract = initialize_abstraction()
    execute_program(abstract)
    abstract.stop_program_timer()
    quit()


if __name__ == "__main__":
    execute_abstractor()