# book_recsys

## code structure
```
    book_recsys
    ├── _install
    │   └── install.sh
    ├── logs
    ├── ml
    │   ├── config.py
    │   ├── utils.py
    │   ├── query.py
    │   ├── download_datas.py
    │   ├── wordclouds.py
    │   └── book_recsys.py
    ├── resources
    │   ├── config_prd.yaml
    │   └── project.db
    └── results
```

## process
```
cd file_path/
```

```
python download_datas.py
```

```
python wordclouds.py
```

```
python book_recsys.py
```