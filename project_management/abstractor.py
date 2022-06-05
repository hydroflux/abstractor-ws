from project_management.timers import start_program_timer
from settings.driver import create_webdriver

from engines.eagle.execute import execute_name_search as eagle_name_search
from engines.eagle.execute import execute_program as execute_eagle
from engines.jaguar.execute import execute_program as execute_jaguar
from engines.leopard.execute import execute_program as execute_leopard
from engines.octopus.execute import \
    execute_legal_search as execute_octopus_legal
from engines.rabbit.execute import execute_name_search as rabbit_name_search
from engines.rabbit.execute import execute_program as execute_rabbit
from engines.rattlesnake.execute import execute_early_document_download
from engines.rattlesnake.execute import execute_program as execute_rattlesnake
from engines.tiger.execute import execute_program as execute_tiger

from project_management.user_prompts import (add_download_type,
                                             currently_unavailable)


def engine_switch(abstract):
    if abstract.county.engine == 'eagle':
        abstract.headless = False
        if abstract.program in ["execute", "review", "download"]:
            return execute_eagle
            # return execute_eagle(abstract)
        elif abstract.program == "name_search":
            return eagle_name_search
            # return eagle_name_search(abstract)
    elif abstract.county.engine == 'jaguar':
        if abstract.program in ["execute", "review", "download"]:
            return execute_jaguar
            # return execute_jaguar(abstract)
    elif abstract.county.engine == 'leopard':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_leopard
            # return execute_leopard(abstract)
    elif abstract.county.engine == 'octopus':
        if abstract.program in ["legal"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_octopus_legal
            # return execute_octopus_legal(abstract)
    elif abstract.county.engine == 'tiger':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_tiger
            # return execute_tiger(abstract)
    elif abstract.county.engine == 'rabbit':
        if abstract.program in ["execute", "review", "download"]:
            return execute_rabbit
            # return execute_rabbit(abstract)
        elif abstract.program == "name_search":
            return rabbit_name_search
            # return rabbit_name_search(abstract)
    elif abstract.county.engine == 'rattlesnake':
        if abstract.program in ["execute", "review", "download"]:
            # Need an additional prompt to handle early document downloads
            # BAD PRACTICE
            if abstract.program == 'download':
                return execute_early_document_download
                # return execute_early_document_download(abstract)
            if abstract.program == 'execute':
                add_download_type(abstract)
            return execute_rattlesnake
            # return execute_rattlesnake(abstract)
    else:
        print(f'"{abstract.county}" does not match available execution options, please review.')
        return False


def execute_program(abstract):
    abstractor = engine_switch(abstract)
    if abstractor is None:
        currently_unavailable(abstract)
    elif abstractor is False:
        quit()
    else:
        browser = create_webdriver(abstract)
        abstract.timer = start_program_timer(abstract)
        abstractor(browser, abstract)
