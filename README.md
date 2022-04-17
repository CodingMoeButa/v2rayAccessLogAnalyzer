# v2rayAccessLogAnalyzer
## 使用方法
1. 安装依赖：
```bash
pip3 install requests
```
2. 购买[IP归属地址查询（含全球版）【支持IPv6】【高并发、不限流、毫秒级】【集群服务】](https://market.aliyun.com/products/57000002/cmapi031829.htm)获得AppCode，填入analyze.py的`APPCODE`常量；
3. 在命令行中运行：
```bash
python analyze.py /path/to/access.log /path/to/analyze.csv
```
