import sys

# from engines.rattlesnake.download_early_documents import download_early_documents
from engines.rattlesnake.execute import execute_early_document_download

sys.path.append(".")

if __name__ == '__main__':
    # from armadillo.execute import execute_program as execute_armadillo
    # from crocodile.execute import execute_name_search as name_search_crocodile
    # from crocodile.execute import execute_program as execute_crocodile
    # from crocodile.execute import execute_review as review_crocodile
    from engines.eagle.execute import execute_name_search as eagle_name_search
    from engines.eagle.execute import execute_program as execute_eagle
    from engines.jaguar.execute import execute_program as execute_jaguar
    from engines.leopard.execute import execute_program as execute_leopard
    from engines.octopus.execute import execute_legal_search as execute_octopus_legal
    from engines.tiger.execute import execute_program as execute_tiger
    from engines.rabbit.execute import execute_program as execute_rabbit
    from engines.rabbit.execute import execute_name_search as rabbit_name_search
    from engines.rattlesnake.execute import execute_program as execute_rattlesnake
    # from rattlesnake.execute import execute_early_document_download as download_rattlesnake
    from settings.initialization import initialize_abstraction
    from project_management.user_prompts import currently_unavailable, add_download_type


print("environment", __name__)


def execute_program(abstract):
    if abstract.county.engine == 'armadillo':
        pass
        # if program_type == 'execute' or program_type == 'download':
        #     add_download_type(county, document_list)
        #     if program_type == 'execute':
        #         execute_armadillo(county, target_directory, document_list, file_name)
        #     else:
        #         execute_armadillo(county, target_directory, document_list, file_name, download_only=True)
        # elif program_type == 'review':
        #     execute_armadillo(county, target_directory, document_list, file_name, review=True)
        # else:
        #     currently_unavailable(county, program_type)
    elif abstract.county.engine == 'crocodile':
        pass
        # if program_type == 'execute':
        #     execute_crocodile(county, target_directory, document_list, file_name)
        # elif program_type == 'review':
        #     review_crocodile()
        # elif program_type == 'name_search':
        #     name_search_crocodile(county, target_directory, search_name)
        # else:
        #     currently_unavailable(county, program_type)
    elif abstract.county.engine == 'eagle':
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
    # elif abstract.county.engine == 'mountain_lion':
    #     if abstract.program in ["execute", "review", "download"]:
    #         if abstract.program == "download":
    #             abstract.headless = False
    #         execute_leopard(abstract)
    #     else:
    #         currently_unavailable(abstract)
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
            # if abstract.program == "download":
            # abstract.headless = False
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
