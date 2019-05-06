# python_example_test

## 怎么在生产环境部署python相关依赖包
1. 取一台和生产环境一样的机器，32位或则64位即可，然后将运行环境安装配置好
2. 将/usr/local/lib/python2.7/dist-packages中的环境全部copy到被隔离的生产环境然后进行测试
