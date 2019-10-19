# 基于遥感影像的建筑物轮廓提取框架

从符合 WMTS 标注的遥感影像中，使用基于深度学习的 [RoboSat.geoc](https://github.com/geocompass/robosat_geoc) 库，提供可视化的 Web 页面，方便的进行训练和预测。并提供服务 `RESTful` 标准的建筑物提取接口，可以用于工程实践生产环境中。



<p align=center>
  <a href="https://github.com/geocompass/rs_buildings_extraction"><img src="https://raw.githubusercontent.com/geocompass/rs_buildings_extraction/master/docs/img/web_map.jpeg" alt="基于 RoboSat.geoc 的建筑物轮廓提取框架" /></a>
</p>



## 主要功能：

- Web 地图方式浏览已有的建筑物轮廓训练样本标注数据，支持显示与隐藏控制
- 一键拉框选取待训练的区域，开始自动化训练
- 一键拉框选取待预测区域，预测结果自动加载到 Web 地图中
- 支持切换天地图（CGCS2000 坐标系）或谷歌（WGS84 坐标系）的遥感影像底图
- 支持查看当前训练日志
- 提供符合 WMTS 的天地图和谷歌地图服务的 XYZ 代理
- 提供符合 `RESTful` 标准的训练和预测接口，可以用于工程生产环境

## 如何安装：

- 下载项目：`git clone https://github.com/geocompass/rs_buildings_extraction.git`
- 进入目录：`cd rs_buildings_extraction`
- 安装依赖：
  - `python install -r requirements.txt` （若使用 Anaconda 需要注意 python 路径，后同）
  - 将 [RoboSat_geoc](https://github.com/geocompass/robosat_geoc/) 安装为系统Package，供本项目调用，安装方法见 [如何作为Packages](https://github.com/geocompass/robosat_geoc/blob/master/README.md#如何作为-packages)
- 项目参数配置：
  - 设置 PostgreSQL 数据库连接： `app/config/secure.py` 中的 `SQLALCHEMY_DATABASE_URI`
  - 设置已有建筑物数据表名称：`app/config/setting.py` 中的 `BUILDINGS_TABLE`
  - 配置文件或训练结果数据路径：`app/config/setting.py` 中的 `ROBOSAT_DATA_PATH`
  - 自动生成的待训练或预测的临时数据集路径：`app/config/setting.py` 中的 `ROBOSAT_DATASET_PATH`
- 运行项目：
  - 前台运行：`python main.py` 
  - 后台运行：`python main.py &`



## 项目依赖

- [RoboSat_geoc](https://github.com/geocompass/robosat_geoc/) ，并将其安装到系统 Packages
- PostgreSQL + PostGIS
- Python 3.6 以上



## Key words：

**IoU:**
Intersection of Union, main index for evaluation on the precision of model. Mathmetically expressed as: Area of I / Area of U, indicating the coefficiency of sample boundary and prediction boundary. This index is appalied to many cases of deep learning, being irrelevant to the process of model and optimal reflection on the model.



## 本项目作者:

- 吴灿 https://github.com/wucangeo
- Liii18 https://github.com/liii18

