import multiprocessing as mp
import multiprocessing.queues as mpq
import threading

class UniqueQueue(mpq.Queue):
    manager = mp.Manager()
    all_items = manager.dict()

    def __init__(self, *args, **kwargs):
        ctx = mp.get_context()
        super(UniqueQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def put(self, item, block=True, timeout=None):
        if item not in self.all_items:
            self.all_items[item] = 1
            mpq.Queue.put(self, item, block, timeout)
            return True
        return False

    def task_done(self, item):
        del self.all_items[item];
