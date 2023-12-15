# 『実験から始める経済学の第一歩』 実験プログラム

花木伸行・島田夏美『実験から始める経済学の第一歩』（2023，有斐閣）で用いる oTree (Chen et al., 2016, J Behav Exp Finance) のプログラムです．

有斐閣 ウェブサポートページ: [https://www.yuhikaku.co.jp/books/detail/9784641151178](https://www.yuhikaku.co.jp/books/detail/9784641151178)

プログラムは oTree v5.10.4 で動作確認をしております．


## Issues

プログラムのバグを発見されたり，改良案を思いつかれたりしたときは，Issues に投稿してください．
回答にはお時間をいただきますが，ご了承ください．


## 動かし方

このプログラムを動かすためには，oTree が動作する環境を用意する必要があります．

### oTree Hub 経由で Heroku を使用する方法

1. Heroku ([https://jp.heroku.com/home](https://jp.heroku.com/home)) のアカウントを作成する．

1. Herokuにログインし，「New」→「Create new app」をクリックし，新しいappを作成する．

1. oTree Hub ([https://www.otreehub.com/](https://www.otreehub.com/)) のアカウントを作成する．

1. oTree Hubで「Heroku」→「Connect to Heroku」をクリックし，oTree HubのアカウントとHerokuのアカウントを紐づけする．

1. アカウントの紐づけに成功すると，oTree Hub上で，先ほどHerokuで作成したappが表示されるはず．そのappの「Register」をクリックする．

1. 「Deploy」をクリックし，`IntroEconBook.otreezip` をアップロードする．自動的にビルドが始まります．

1. 「Configure」でHerokuの料金プランを設定する．

    なお，2023年12月時点で，Herokuに無料プランはありません．

1. 「Heroku Projects」ページでapp名の横のリンクのアイコンをクリックするとoTreeの管理者画面へアクセスできる．



### 自分のPCで環境を整備する方法

（参考）[https://yshimod.github.io/otree5-seminar/server_setup/](https://yshimod.github.io/otree5-seminar/server_setup/)

1. Pythonをインストールする．

1. pipでoTreeと必要なライブラリをインストールする．

    ```
    cd /your/path/to/IntroEconBook
    pip install -r requirements.txt
    ```

    または
    ```
    pip install otree
    ```

1. oTreeサーバを起動には以下のコマンドを実行する．

    ```
    otree prodserver
    ```

1. ブラウザで localhost:8000 にアクセスすると，管理者画面にアクセスできる．

1. oTreeサーバを終了するには Ctrlキー + C を押す．



### 自分のPCでDockerを使って環境を整備する方法

- Pythonの環境を整備するのは意外と面倒．
- すでに研究の他の用途（たとえばデータ解析）でPythonを使っている場合，oTreeを導入することで既存の環境が汚染されてしまうかもしれない．
- Dockerを使う方法は，自分でPythonをインストールする必要はないし，すでにあるPython環境に影響を与えないため，便利．

1. Docker Desktop ([https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)) をインストールする．

1. ビルドする．

    ```
    cd /your/path/to/IntroEconBook
    docker compose build
    ```

1. 起動する（`prodserver`）には以下のコマンドを実行する．

    ```
    docker compose up -d
    ```

    Notes: `compose.yaml` において，デフォルトのコマンドとして `otree prodserver` を設定してある．

1. ブラウザで localhost:8000 にアクセスすると，管理者画面にアクセスできる．

    ユーザー名は`admin`，パスワードは`0099`に設定してある．
    パスワードを変更するには`.env`ファイルの`OTREE_ADMIN_PASSWORD`の値を変更する（変更後の`.env`ファイルは外部に公開しないこと）．

1. oTreeサーバを終了するには以下のコマンドを実行する．

    ```
    docker compose down
    ```

1. Postgresデータベースをリセットするには（`docker compose up -d` を実行した状態で）以下のコマンドを実行する．

    ```
    docker compose exec otreeserver otree resetdb
    ```

1. （`docker compose up -d` の状態が続いているとき）コードを編集したあと反映させるには以下のコマンドを実行する．

    ```
    docker compose restart
    ```

1. コードの編集中にサーバーを起動する（`devserver`）には以下のコマンドを実行する．

    ```
    # 初回のみ
    docker build ./ -t devotree

    # このコマンドで devserver を起動
    docker run --rm -it -v $PWD:/app -p 8000:8000 devotree
    ```

    Notes: `Dockerfile` において，デフォルトのコマンドとして `otree devserver 0.0.0.0:8000` を設定してある．
