> 特别感谢两位学长：[hewei2001](https://github.com/hewei2001/campus-canteen-ordering/commits?author=hewei2001) [pinskyrobin](https://github.com/pinskyrobin) 留下的参考！

基于Django+Bootstrap+Mysql实现的食堂外送点餐系统。具体效果可见[演示视频](./演示视频.mp4)。

实现了以下功能（划线部分）：

> 1. ~~用户注册（普通用户、食堂管理员、商家);~~
> 2. ~~食堂管理员可进行食堂信息维护(新增、修改、删除);~~
> 3. 商家可进行商铺维护(新增、修改、删除);
> 4. ~~商家可进行菜品维护(新增、修改、删除);~~
> 5. ~~普通用户可浏览菜品、下订单~~（~~选择某个食堂、某个商家的某些菜品，设置购买数量~~，设置外送地址，设置联系方式..….) ;
> 6. ~~商家可浏览订单、接单（修改订单状态)。~~

由于是速通学习，故而前端界面没有经过雕琢，代码也写得比较乱，一些逻辑也没太严谨，不过主打一个能润（）

简单的运行命令：

```bahs
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

