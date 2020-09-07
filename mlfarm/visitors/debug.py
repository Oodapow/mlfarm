from mlfarm.visitors.core import BaseVisitor

class PrintVisitor(BaseVisitor):
    def visit_obj(self, obj):
        print(obj)
        return obj

    def visit_str(self, obj):
        print(obj)
        return obj

    def visit_list(self, obj):
        print(obj)
        return obj

    def visit_dict(self, obj):
        print(obj)
        return obj
