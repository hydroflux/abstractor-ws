import sys

sys.path.append(".")

if __name__ == '__main__':
    from engines.eagle.execute import execute_name_search as eagle_name_search
    from engines.eagle.execute import execute_program as execute_eagle
    from engines.jaguar.execute import execute_program as execute_jaguar
    from engines.leopard.execute import execute_program as execute_leopard
    from engines.octopus.execute import \
        execute_legal_search as execute_octopus_legal
    from engines.rabbit.execute import \
        execute_name_search as rabbit_name_search
    from engines.rabbit.execute import execute_program as execute_rabbit
    from engines.rattlesnake.execute import execute_early_document_download
    from engines.rattlesnake.execute import \
        execute_program as execute_rattlesnake
    from engines.tiger.execute import execute_program as execute_tiger
    from project_management.user_prompts import (add_download_type,
                                                 currently_unavailable)
    from settings.initialization import initialize_abstraction


print("environment", __name__)


def execute_program(abstract):
    if abstract.county.engine == 'eagle':
        abstract.headless = False
        if abstract.program in ["execute", "review", "download"]:
            execute_eagle(abstract)
        elif abstract.program == "name_search":
            eagle_name_search(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'jaguar':
        if abstract.program in ["execute", "review", "download"]:
            execute_jaguar(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'leopard':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            execute_leopard(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'octopus':
        if abstract.program in ["legal"]:
            if abstract.program == "download":
                abstract.headless = False
            execute_octopus_legal(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'tiger':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            execute_tiger(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'rabbit':
        if abstract.program in ["execute", "review", "download"]:
            execute_rabbit(abstract)
        elif abstract.program == "name_search":
            rabbit_name_search(abstract)
        else:
            currently_unavailable(abstract)
    elif abstract.county.engine == 'rattlesnake':
        if abstract.program in ["execute", "review", "download"]:
            # Need an additional prompt to handle early document downloads
            # BAD PRACTICE
            if abstract.program == 'download':
                execute_early_document_download(abstract)
            if abstract.program == 'execute':
                add_download_type(abstract)
            execute_rattlesnake(abstract)
        else:
            currently_unavailable(abstract)
    else:
        print(f'"{abstract.county}" does not match available execution options, please review.')


def execute_abstractor():
    abstract = initialize_abstraction()
    execute_program(abstract)
    abstract.stop_program_timer()
    quit()


execute_abstractor()
