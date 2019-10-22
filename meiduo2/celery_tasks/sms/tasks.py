from libs.yuntongxun.sms import CCP
from ..main import app
import logging
logger = logging.getLogger()

@app.task(bind=True,default_retry_delay=10)
def sms_send(self,mobile,random_code):
    try:
        rect = CCP().send_template_sms(mobile, [random_code, 2], 1)
    except Exception as e:
        logger.error(e)
        return self.retry(exc=e,max_retries=3)

    if rect!=0:
        return self.retry(exc=Exception('发送失败'),max_retries=3)