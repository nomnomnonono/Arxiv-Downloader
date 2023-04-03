import argparse
import os

from omegaconf import OmegaConf
from scrape import save_config, scrape_paper


def argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="File path for config file.",
    )
    args = parser.parse_args()
    return args


def main(args):
    config = OmegaConf.load(args.config)
    os.makedirs(config.base_dir, exist_ok=True)
    config = scrape_paper(config)
    save_config(config, args.config)


if __name__ == "__main__":
    args = argparser()
    main(args)
