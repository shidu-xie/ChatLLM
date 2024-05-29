# 法律RAG模型

* 2024/05/26 创建仓库
* 安装所需的库
```commandline
pip install langchain -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install langchain_openai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install zhipuai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install redis -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install langchain_community -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install Crypto -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install  pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install  openai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install  requests_toolbelt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
* 配置服务器
  * 操作系统 阿里云CentOS 7.9 64位 SCC版
  * 开放服务器端口 新建安全组 实例加入安全组
  * 安装nginx 
    https://blog.csdn.net/lxh_worldpeace/article/details/107013311 
    https://blog.csdn.net/Hjingeng/article/details/105264814
  * 安装【anaconda】
    https://blog.csdn.net/wyf2017/article/details/118676765
  * 安装Crypto的bug
    https://blog.csdn.net/xiaojin21cen/article/details/109642940


* 配置redis
  * windows https://blog.csdn.net/qq_45938544/article/details/131088850
  * linux https://blog.csdn.net/m0_51285952/article/details/123423799


* 创建应用
* 验证服务器，接收消息
* 设置可信ip

