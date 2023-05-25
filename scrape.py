import datetime
import os
import time

import arxiv
import pandas as pd
import yaml
from omegaconf import OmegaConf
from tqdm import tqdm


def scrape_paper(config: OmegaConf) -> OmegaConf:
    """
    論文情報の取得を行う

    Args:
        config (OmegaConf): 設定ファイル

    Returns:
        OmegaConf: 更新後の設定ファイル
    """

    if os.path.exists(os.path.join(config.base_dir, f"{config.tag}.csv")):
        df = pd.read_csv(os.path.join(config.base_dir, f"{config.tag}.csv"))
    else:
        df = pd.DataFrame(
            [], columns=["title", "abstract", "author", "year", "month", "link"]
        )

    idx = max(df.index) if len(df) > 0 else 0

    time_query, config = define_time_range(config)
    query = config.query + " AND " + time_query
    search = arxiv.Search(
        query=query,
        max_results=config.max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    for result in tqdm(search.results()):
        year, month, _ = str(result.published).split(" ")[0].split("-")
        df.loc[idx] = [
            result.title.replace("'", "").replace('"', ""),
            result.summary.replace("'", "").replace('"', ""),
            str(result.authors[0]),
            int(year),
            int(month),
            str(result.links[0]),
        ]
        if config.download_pdf:
            result.download_pdf(dirpath=os.path.join(config.base_dir, config.tag))
            time.sleep(10)

        idx += 1

    df.to_csv(os.path.join(config.base_dir, f"{config.tag}.csv"), index=False)

    return config


def define_time_range(config: OmegaConf) -> tuple[str, OmegaConf]:
    """
    いつから取得を行うかの情報取得と最終取得時刻の更新を行う

    Args:
        config (OmegaConf): 設定ファイル

    Returns:
        tuple[str, OmegaConf]: 取得開始時刻と更新後の設定ファイル
    """

    now = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
    time_query = f"submittedDate:[{config.before} TO {now}]"
    config["before"] = now
    return time_query, config


def save_config(config: OmegaConf, file_path: str) -> None:
    """
    設定ファイルを保存する

    Args:
        config (OmegaConf): 設定ファイル
        file_path (str): 保存先ファイルパス
    """

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(dict(config), f, allow_unicode=True, default_flow_style=False)
