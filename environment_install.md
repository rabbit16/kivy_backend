# 安装mysqlclient记录
`sudo apt-get install libmysqlclient-dev`

# 创建超级管理员
    python manage.py createsuperuser

# 创建app
    python manage.py startapp <appName>

# 解决mysql不加sudo报错问题
    1.ubuntu安装mysql默认用户名和密码：
    
    sudo cat /etc/mysql/debian.cnf
    2.ubuntu修改root密码
    
    先登录超级管理员，即步骤一的用户名和密码。
    
    use mysql;
    ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
    
        1
        2
    
    3. 登录报错&&但是sudo可以正常登录：
    
    ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
    解决办法：
    
    sudo vim /etc/mysql/my.cnf
    添加以下内容：
    
    [mysqld]
    socket=/tmp/mysql.sock
    [client]
    socket=/tmp/mysql.sock
    
        1
        2
        3
        4
    
    重启mysql服务
    service mysql restart