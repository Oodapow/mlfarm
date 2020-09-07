import importlib

class ClassBuilder:
    def __init__(self, _class, args):
        split = _class.split('.')
        self._class = getattr(importlib.import_module('.'.join(split[:-1])), split[-1])
        self.args = args
    
    def __call__(self, args=None):
        if (not self.args) and args:
            self.args = args
        elif self.args and args:
            if isinstance(self.args, dict) and isinstance(args, dict):
                self.args.update(args)

        if not self.args:
            obj = self._class()
        elif isinstance(self.args, list):
            obj = self._class(*self.args)
        elif isinstance(self.args, dict):
            obj = self._class(**self.args)
        else:
            obj = self._class(self.args)
        
        if isinstance(obj, Generator):
            return list(obj)

        return obj

class Generator:
    def __init__(self, data, times=1):
        self.data = data
        self.times = times

    def __getitem__(self, index):
        if index >= self.times:
            raise IndexError
        return self.process(index)

    def __len__(self):
        return self.times
    
    def process(self, index):
        return self.data

class BaseVisitor:
    def visit(self, obj):
        if isinstance(obj, dict):
            return self.visit_dict(obj)
        elif isinstance(obj, list):
            return self.visit_list(obj)
        elif isinstance(obj, str):
            return self.visit_str(obj)
        else:
            return self.visit_obj(obj)

    def visit_obj(self, obj):
        return obj

    def visit_str(self, obj):
        return obj

    def visit_list(self, obj):
        return [self.visit(o) for o in obj]

    def visit_dict(self, obj):
        return dict([(k, self.visit(v)) for k, v in obj.items()])

class CompositeVisitor(BaseVisitor):
    def __init__(self, *args):
        self.args = args

    def visit(self, obj):
        for visitor in self.args:
            obj = visitor.visit(obj)
        return obj

class ContextVisitor(BaseVisitor):
    path = []

    def visit(self, obj):
        self.path.append(obj)
        res = super().visit(obj)
        self.path.pop()
        return res

class ClassVisitor(BaseVisitor):
    def visit_dict(self, obj):
        if not obj.get('class', False):
            return super().visit_dict(obj)

        builder = ClassBuilder(
            obj['class'], 
            self.visit(obj.get('args', None))
        )

        if obj.get('builder', False):
            return builder

        return builder()