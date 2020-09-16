from mlfarm.core import ContextAwareVisitor

class PrintTableVisitor(ContextAwareVisitor):
    '''
    '''
    def visit_obj(self, obj):
        return f'{self.get_path()}, {obj}\n'

    def visit_str(self, obj):
        return f'{self.get_path()}, {obj}\n'

    def visit_list(self, obj):
        res = super().visit_list(obj)
        return ''.join(res)

    def visit_dict(self, obj):
        res = super().visit_dict(obj)
        return ''.join(res.values())

if __name__ == "__main__":
    import doctest
    doctest.testmod()