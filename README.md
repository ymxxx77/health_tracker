# 健康管家 Health Tracker

用 Django 写的轻量健康数据记录工具。把饮食、运动这类零散记在备忘录里的数据，
变成有结构、能筛选、能自动汇总的记录。

## 功能
- 运动、饮食记录的新增 / 编辑 / 删除 / 查询
- 全部 / 本周 / 本月 三档时间筛选
- 自动统计本周、本月的运动次数与饮食总热量
- 输入校验与重复提交拦截，避免脏数据

## 技术栈
Python · Django · SQLite · HTML/CSS

## 运行
```bash
git clone https://github.com/ymxxx77/health_tracker.git
cd health_tracker/Health_tracker
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
