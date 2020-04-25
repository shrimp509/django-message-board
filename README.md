# 好想留言板（後端專案）

-> 留言板前端頁面：[留言板連結](http://yun-ru-tseng.gitlab.io/messageboard/#/messageBoard)

## 專案需求
[需求連結](https://www.notion.so/2020-03-28-91a6c9702f4f4238bdbbdb9f65580a59)

![需求圖](https://github.com/shrimp509/django_message_board/blob/master/screenshots/requirement.png)

## 畫面截圖

### 登入
![登入圖](https://github.com/shrimp509/django_message_board/blob/master/screenshots/login.png)

### 可發表文章、針對文章留言(第一層)、針對留言來留言(第二層留言)
![留言板圖](https://github.com/shrimp509/django_message_board/blob/master/screenshots/board.png)

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


## 透過 Notion 進行專案管理
### [專案文件](https://www.notion.so/a0ea05abf82d4527a38447865a898cb4)
![專案文件圖](https://github.com/shrimp509/django_message_board/blob/master/screenshots/document.png)

### [專案時程](https://www.notion.so/8c0b93cae14540dba3f6ecef7b5275e5)
![專案時程圖_ruru](https://github.com/shrimp509/django_message_board/blob/master/screenshots/develop_cards_ruru.png)
![專案時程圖_sam](https://github.com/shrimp509/django_message_board/blob/master/screenshots/develop_cards_sam.png)