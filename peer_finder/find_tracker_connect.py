import socket
from threading import Thread
from queue import Queue
from threading import Lock

def check(in_queue, out_queue, lock):
    '''
    Checks if tracker target is a viable connection.
    '''
    target = in_queue.get()


    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.settimeout(10)
    try:
        sock.connect(target)
        if lock.locked():
            sock.close()
            in_queue.task_done()
            return False
        lock.acquire()
        sock.close()
        out_queue.put(target)
        in_queue.task_done()
        return True
    except socket.error:
        sock.close()
        pass
    in_queue.task_done()

def target_segment(seq, size=8):
    '''This function segments a large list of connection targets into smaller lists of 8 or less targets.
    '''
    if len(seq) <= 8:
        return [seq]
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def form_connection(target_segs):
    '''Handles multithreding for connecting to multiple targets at a time.
    '''

    for inner_list in target_segs:
        lock = Lock()
        in_queue = Queue()
        out_queue = Queue()

        for target in inner_list:
            worker = Thread(target=check, args=(in_queue, out_queue, lock))
            worker.daemon = True
            worker.start()

        for target in inner_list:
            in_queue.put(target)

        in_queue.join()

        if not out_queue.empty():
            return out_queue.get()

    raise socket.error

def run(target_list):
    '''Coordinates connecting to targets.
    '''
    target_segs = target_segment(target_list)
    connection = form_connection(target_segs)
    return connection





