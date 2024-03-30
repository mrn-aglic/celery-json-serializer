from celery_json.celeryapp import app


@app.task(bind=True)
def printer(self, task_arg):
    print(task_arg)


@app.task
def some_task(*arg, a=None, b=None, c=None):
    print(f"print task args: a: {a}, b: {b}, c: {c}")


@app.task
def pipeline():
    return printer.s(some_task.s([1, 2, 3], a=15)).apply_async()