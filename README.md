# visplatform
1 测试修改

2 本地修改



# 安装

有两个visplatform目录我们把虚拟环境创建在第一层vispaltform目录，激活以后切换进 visplatform/visplatform 目录对应的子目录再执行 flask run 命令来启动程序。

### 克隆仓库

```
$ git clone https://github.com/935462955/visplatform.git
$ cd visplatform
```

### 创建 & 激活虚拟环境 & 安装依赖包

使用 Pipenv：

```
$ pipenv install --dev
$ pipenv shell
```

如果你还没有安装Pipenv，那么可以在运行`pipenv`命令前通过pip安装（`pip install pipenv`）。

### 运行示例程序

```
$ cd visplatform/visplatform
$ flask run
```

# 其他软件

### IDE

推荐使用pycharm来作为IDE开发

### 数据库

MongoDB