# python_example_test

## 怎么在生产环境部署python相关依赖包
1. 取一台和生产环境一样的机器，32位或则64位即可，然后将运行环境安装配置好
2. 将/usr/local/lib/python2.7/dist-packages中的环境全部copy到被隔离的生产环境然后进行测试

## 没有root权限怎么部署python相关依赖包
1. 安装到指定目录`python3 setup.py install --prefix=/home/share/python/lib/`
2. 在代码中import之前插入如下语句, 这样在import之前执行改语句能导入第三方包路径
```python3
import sys
sys.path.append('/home/share/python/lib/python3.6/site-packages/pycryptodomex-3.8.1-py3.6-linux-x86_64.egg')
from Cryptome.Publickey import RSA
```

## 怎么离线安装第三方包
### whl文件
1. 在`https://www.lfd.uci.edu/~gohlke/pythonlibs/` 中找到对应的`whl文件`下载
2. `pip3 install *.whl` 安装第三方包.
### setup.py安装 
**设置PYTHONPATH**
`export PYTHONPATH="/home/share/python/lib/python3.6/site-packages:$PYTHONPATH"`
1. 源码安装到指定目录`python3 setup.py install --prefix=/home/share/python/lib/`
