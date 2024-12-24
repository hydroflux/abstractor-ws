from project_management.timers import start_program_timer
from settings.driver import create_webdriver

from engines.armadillo.execute import execute_program as execute_armadillo
from engines.armadillo.execute import execute_name_search as armadillo_name_search
from engines.buffalo.execute import execute_program as execute_buffalo
from engines.dolphin.execute import execute_program as execute_dolphin
from engines.eagle.execute import execute_name_search as eagle_name_search
from engines.eagle.execute import execute_program as execute_eagle
from engines.jaguar.execute import execute_program as execute_jaguar
from engines.komodo.execute import execute_program as execute_komodo
from engines.leopard.execute import execute_program as execute_leopard
from engines.manta_ray.execute import execute_program as execute_manta_ray
from engines.octopus.execute import \
    execute_legal_search as execute_octopus_legal
from engines.platypus.execute import \
    execute_legal_search as execute_platypus_legal
from engines.rabbit.execute import execute_name_search as rabbit_name_search
from engines.rabbit.execute import execute_program as execute_rabbit
from engines.rattlesnake.execute import execute_early_document_download
from engines.rattlesnake.execute import execute_program as execute_rattlesnake
from engines.swordfish.execute import execute_program as execute_swordfish
from engines.tiger.execute import execute_program as execute_tiger

from project_management.user_prompts import (add_download_type,
                                             currently_unavailable)


def engine_switch(abstract):
    if abstract.county.engine == 'armadillo':
        abstract.headless = False
        if abstract.program in ["execute", "review", "download"]:
            return execute_armadillo
        elif abstract.program == "name_search":
            return armadillo_name_search
    elif abstract.county.engine == 'buffalo':
        abstract.headless = False
        if abstract.program in ["execute", "review", "download"]:
            return execute_buffalo
    elif abstract.county.engine == 'dolphin':
        if abstract.program in ["execute", "review", "download", "legal"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_dolphin
    elif abstract.county.engine == 'eagle':
        abstract.headless = False
        if abstract.program in ["execute", "review", "download"]:
            return execute_eagle
        elif abstract.program == "name_search":
            return eagle_name_search
    elif abstract.county.engine == 'jaguar':
        if abstract.program in ["execute", "review", "download"]:
            return execute_jaguar
    elif abstract.county.engine == 'komodo':
        if abstract.program in ["execute", "review", "name_search"]:
            return execute_komodo
    elif abstract.county.engine == 'leopard':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_leopard
    elif abstract.county.engine == 'manta_ray':
        if abstract.program in ["execute", "review", "download", "legal", "register_page_count"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_manta_ray
    elif abstract.county.engine == 'octopus':
        if abstract.program in ["execute", "review", "download", "legal"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_octopus_legal
    elif abstract.county.engine == 'platypus':
        if abstract.program in ["legal"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_platypus_legal
    elif abstract.county.engine == 'rabbit':
        if abstract.program in ["execute", "review", "download"]:
            return execute_rabbit
        elif abstract.program == "name_search":
            return rabbit_name_search
    elif abstract.county.engine == 'rattlesnake':
        if abstract.program in ["execute", "review", "download"]:
            # Need an additional prompt to handle early document downloads
            # BAD PRACTICE
            if abstract.program == 'download':
                return execute_early_document_download
            if abstract.program == 'execute':
                add_download_type(abstract)
            return execute_rattlesnake
    elif abstract.county.engine == 'swordfish':
        if abstract.program in ["execute", "review", "download", "legal", "register_page_count"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_swordfish
    elif abstract.county.engine == 'tiger':
        if abstract.program in ["execute", "review", "download"]:
            if abstract.program == "download":
                abstract.headless = False
            return execute_tiger
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
