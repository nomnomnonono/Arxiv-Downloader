# Arxiv-Downloader
## 概要
arxivから自動で任意の論文を自動で取得できるCUIアプリケーション

## 実行方法
```bash
poetry run python main.py --config config.yaml
```

## 設定ファイル（config.yaml）の詳細
取得したい論文の分野（`tag`）ごとに設定ファイルを作成することを想定。
- `base_dir`：ベースとなるディレクトリ
- `before`：前回の取得日時（YYMMDDHHMMSS形式）。初回以降は自動で更新されるが、初回は自分で取得したい最も遅い時点を記載する。
- `max_results`：最大取得論文数
- `query`：論文を取得するクエリ。タイトルやタグ、アブストを指定できる。詳細は[公式ドキュメント](https://pypi.org/project/arxiv/)を参照。
- `tag`：設定ファイルのタグ。例えばセグメンテーション用の設定ファイルには`Segmentation`のようにつけることで、取得した論文をフォルダ分けすることができる。

## 便利な使い方
スクリプトを実行して得られた論文をローカルPCに保存・閲覧するだけでも有用であるが、さらに便利な使い方を提供する。

それは[PC版のGoogle Drive](https://www.google.com/intl/ja_jp/drive/download/)を使うことです。リンク先からダウンロードし、設定で論文が自動で保存されるフォルダをGoogle Driveに自動バックアップするように設定することで、いつでも・どこでも取得した論文を閲覧することができるようになります。
