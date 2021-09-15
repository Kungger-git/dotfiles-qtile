#!/bin/python

import shutil

def format_bytes(num_bytes):
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while num_bytes > power:
        num_bytes /= power
        n += 1
    return f"{round(num_bytes, 2)}{power_labels[n]}b"

def diskspace():
    total, used, free = shutil.disk_usage('/')
    data_disk = {
        'DiskUsage': f'{format_bytes(total)} / {format_bytes(free)}',
        'FreeSpace': f'{format_bytes(used)}'
    }
    return data_disk
