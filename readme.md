# chaoxing学习通自动化刷课  
：本项目的主要目的是解放双手，实现刷课自由。  
该项目基于python的Selenium完成自动化测试，该项目目前处于测试阶段，可能不太稳定，仅供学习参考交流！  
## 使用说明  
使用前先下载python3.10+  
目前只支持Edge的驱动自动下载（因为驱动最全）
### 源码运行  
1. git clone https://github.com/zhou2004/chaoxing-.git  至本地
2. cd auto_answers
3. pip install -r requirements.txt
4. python download.py (下载对应的驱动)
5. (可选配置文件运行) 复制config_template.ini文件为config.ini文件，修改文件内的账号密码内容, 执行 python auto_answers.py -c config.ini
6. (可选命令行运行)python auto_answers.py -u 手机号 -p 密码 -l 课程ID  

### 题库说明  
需要自己配置可用的api，正确率不做保证，采用的AI模型为GPT-3.5,  
可供学习参考。


###  参考项目
https://github.com/Samueli924/chaoxing