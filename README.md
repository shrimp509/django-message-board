# Django留言板練習題 at 好想

## 專案需求
[需求連結](https://www.notion.so/60bbd52758b64bbc9f80a2d046a9f589)

![](https://github.com/shrimp509/django_message_board/blob/master/screenshots/requirements.png)

## 畫面截圖

登入
![](https://github.com/shrimp509/django_message_board/blob/master/screenshots/login.png)

可發表文章、針對文章留言（僅一層留言）
![](https://github.com/shrimp509/django_message_board/blob/master/screenshots/board.png)

## 未完成
* 僅完成對發文的第一層留言
* 偷用框架、還沒做完QQ
* 留言沒按照新->舊排序
* 自信廢

![](https://imgur.dcard.tw/WDWrBTO.jpg)

## 怎麼使用這個專案？

* 安裝專案相關套件
`$ pip3 install requirements.txt`

* 進行 migrate
`$ python3 manage.py makemigrations`
`$ python3 manage.py migrate`

* 執行專案
`$ python3 manage.py runserver 127.0.0.1:8000`

* 開啟瀏覽器
訪問 `127.0.0.1:8000/login`