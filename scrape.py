import datetime
import time

import arxiv
import yaml
from omegaconf import OmegaConf
from tqdm import tqdm


def scrape_paper(config):
    time_query, config = define_time_range(config)
    query = config.query + " AND " + time_query
    search = arxiv.Search(
        query=query,
        max_results=config.max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    for result in tqdm(search.results()):
        result.download_pdf(dirpath=config.base_dir)
        time.sleep(10)

    return config


def define_time_range(config):
    now = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
    time_query = f"submittedDate:[{config.before} TO {now}]"
    config["before"] = now
    return time_query, config


def save_config(config, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(dict(config), f, allow_unicode=True, default_flow_style=False)
