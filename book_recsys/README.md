# book_recsys

## code structure
- `resources/project.db`는 용량 문제로 업로드하지 않음
```
    book_recsys
    ├── _install
    │   └── install.sh
    ├── ml
    │   ├── config.py
    │   ├── utils.py
    │   ├── query.py
    │   ├── review_keywords.py
    │   └── book_recsys.py
    ├── resources
    │   └── project.db
    └── results
            ├── review_keywords.csv
            └── book_rcmm.csv
```

## process
#### 1. 필요한 패키지 설치
- 실행이 안되는 경우 `bash _install/install.sh`나 `. _install/install.sh`로 실행
- 가상환경을 사용할 경우 line14~17의 주석을 지우고 실행
```
sh _install/install.sh
```

#### 2. 책별 리뷰 키워드 & 유저별 책 추천
- 실행 전에 `config.py`파일에서 `WORKING_DIRECTORY`를 본인의 경로에 맞게 수정
- 아래 py파일들을 실행하며 경로 문제가 발생하는 경우 `book_recsys/ml` 위치에서 실행


- 책별 리뷰 키워드
    - 각 책별로 키워드 10개를 추출
    ```
    python review_keywords.py
    ```

  
- 유저별 책 추천
    - 각 유저별로 25개의 책을 추천하고, 추천된 책을 5개의 카테고리로 구분
    - 이력이 부족한 유저의 경우 -> 평균평점이 4점 이상이고 이용횟수가 많은 책 상위 25개를 추천하고, 책을 5개의 카테고리로 구분
    ```
    python book_recsys.py
    ```
