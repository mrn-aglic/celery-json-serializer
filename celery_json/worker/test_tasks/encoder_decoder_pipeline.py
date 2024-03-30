from celery_json.celeryapp import app
from celery_json.worker.instances import hr_department


@app.task
def producer():
    return hr_department


@app.task
def consumer(hr_department):
    print(hr_department)
    print(f"The type of the variable is: {type(hr_department)}")


@app.task
def pipeline():
    return (producer.s() | consumer.s()).apply_async()
