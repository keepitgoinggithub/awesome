
#### 依赖包
```
pip install jira
pip install pandas
pip install cryptography
pip install flask
```

#### 解决关于xlrd 解析xlsx格式Excel报错
[参考] (https://blog.csdn.net/fivemillion/article/details/126050669)
```
pip install xlrd==1.2.0
打开xlsx.py查找getiterator并替换成iter
```
