# zacui
微信查找已经删除你的好友，网页版实现。

已经放在新浪sae上面了
链接地址：http://wxuser.applinzi.com/

新浪sae上不稳定，找了一下原因，还是cookie的问题，直接用python manage.py runserver 0.0.0.0:8000 没有问题，
用uwsgi跑起来就取不到通讯录的记录了，还是cookie问题。有时间再研究吧。
