# 中间人的配置信息
# 让中间人连接redis的 14号库
broker_url = "redis://127.0.0.1/14"
# 任务执行结果保存在 15号库
result_backend = "redis://127.0.0.1/15"