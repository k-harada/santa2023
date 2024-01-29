# ごりら

Poetry する。

```
poetry install
```

BigQuery テーブル作る（1 回でいい）。

```
poetry run create-table
```

`requirements.txt` 吐き出す。

```
poetry export --output requirements.txt
```

Docker イメージビルドする。

```
docker-compose build
docker-compose push
```