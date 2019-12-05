from queue import Queue

class UniqueQueue(Queue):
    def _init(self, maxsize):
        self.all_items = set()
        Queue._init(self, maxsize)

    def put(self, item, block=True, timeout=None):
        if item not in self.all_items:
            self.all_items.add(item)
            Queue.put(self, item, block, timeout)

    def task_done(self, item):
        self.all_items.remove(item);
        return Queue.task_done(self)
