from rq.job import Job


def check_size_correct(size: str) -> bool:
    if size in ['32', '64', 'original']:
        return True
    return False


def get_status_job(task: Job) -> str:
    status = task.get_status()
    if status in ['finished']:
        return 'DONE'
    if status in ['queued', 'deferred']:
        return 'WAITING'
    if status in ['started']:
        return 'IN_PROGRESS'
    return 'FAILED'
