# 985高校微博爬取

本仓库是天津大学2021硕的大数据分析理论与算法作业的一部分，目的在于通过爬虫手段获取985高校新浪微博过去每一条动态的点赞数、转发数、评论数、发表时间和发表内容，从而进行大数据分析。

## Usage

打开浏览器，登陆手机端微博网站: m.weibo.cn，找个空白的地方右键->检查元素->网络->Fetch/XHR，进入抓包模式。刷新下网页，随便点开一个返回的数据，找到自己的cookie，复制到```craw_weibo.py```代码的cookie部分。

然后直接运行 ```python craw_weibo.py```即可。

## 可以改的地方

代码里可以改的地方一个是cooki，一个是uid。

