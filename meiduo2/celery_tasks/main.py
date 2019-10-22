# from celery import Celery
# # 为celery使用django配置文件进行设置
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo2.settings")
#
# # 创建celery实例
# # celery_app = Celery('celery_tasks')
#
# # 创建实例对象
# app = Celery(main="celery_tasks")
#
# # 从工程加载celery配置
# app.config_from_object('celery_tasks.config')
#
# # 从工程中自动加载
# app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.emails'])

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo2.settings')

app = Celery(main='celery_tasks')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('celery_tasks.config', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.emails'])


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

# celery -A celery_tasks.main worker -l info
# celery -A celery_tasks.main worker -l info -P eventlet -c 1000