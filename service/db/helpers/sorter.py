from sqlalchemy import desc, asc

DEFAULT_SORT_ORDER = 'ASC' # If changed, look at the condition in apply_sorter if self.get_order() == "DESC":.

class Sorter(object):

    def __init__(self, sorter, mappings = []):
        if 'sortby' in sorter:
            self._field = sorter['sortby']

            if 'sort' in sorter:
                self._order = sorter['sort']
            else:
                self._order = DEFAULT_SORT_ORDER

            self._enabled = True
        else:
            self._enabled = False

        self._mappings = mappings

    def is_enabled(self):
        return self._enabled

    def get_order(self):
        return self._order

    def get_field(self):
        return self._field

    def apply_sorter(self, q, cls):
        if self.is_enabled():
            if self.get_field() in self._mappings:
                (cls, field) = self._mappings[self.get_field()]
                attr = getattr(cls, field)
            else:
                attr = getattr(cls, self.get_field())
            if self.get_order() == "DESC": # If changed, look at the DEFAULT_SORT_ORDER definition.
                return q.order_by(desc(attr))
            else:
                return q.order_by(asc(attr))
        else:
            return q
