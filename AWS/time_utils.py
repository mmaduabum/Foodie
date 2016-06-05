import time


def timestamp_to_seconds(stamp):
    pattern = '%Y-%m-%d %H:%M:%S'
    sex = int(time.mktime(time.strptime(stamp, pattern)))
    return sex

