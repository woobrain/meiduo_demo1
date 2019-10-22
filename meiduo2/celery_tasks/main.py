from celery import Celery
# 为celery使用django配置文件进行设置
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo2.settings")

# 创建celery实例
# celery_app = Celery('celery_tasks')

# 创建实例对象
app = Celery(main="celery_tasks")

# 从工程加载celery配置
app.config_from_object('celery_tasks.config')

# 从工程中自动加载
app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.emails'])