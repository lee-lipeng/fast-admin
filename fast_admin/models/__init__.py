import os
import importlib
from tortoise import Model
from inspect import isclass

# 遍历 models 目录中的所有 .py 文件
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # 去掉 .py 后缀
        module_path = f"fast_admin.models.{module_name}"  # 构建模块路径

        # 动态导入模块
        module = importlib.import_module(module_path)

        # 遍历模块中的所有属性
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            # 检查属性是否为类，并且是 Model 的子类
            if isclass(attr) and issubclass(attr, Model):
                globals()[attr_name] = attr  # 将模型类导入当前命名空间
