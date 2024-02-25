from celery.utils.log import get_task_logger

from celery_json.app import config
from celery_json.celeryapp import app
from celery_json.worker.test_tasks import print_task, simple_pipeline

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        if config.is_scheduler():
            return

        app.control.purge()

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
