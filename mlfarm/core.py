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
        
        return obj

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

class ContextAwareVisitor(BaseVisitor):
    path = []

    def get_path(self):
        return ''.join(self.path)

    def visit_list(self, obj):
        i = 0
        res = []
        for o in obj:
            self.path.append(f'[{i}]')
            res.append(self.visit(o))
            self.path.pop()
            i+=1
        return res

    def visit_dict(self, obj):
        res = {}
        for k,v in obj.items():
            self.path.append(k if len(self.path) == 0 else f'.{k}')
            res[k] = self.visit(v)
            self.path.pop()
        return res

class CompositeVisitor(BaseVisitor):
    def __init__(self, *args):
        self.args = args

    def visit(self, obj):
        for visitor in self.args:
            obj = visitor.visit(obj)
        return obj

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

class GraphVisitor(ContextAwareVisitor):
    path = ['cluster']

    def __init__(self, g):
        self.g = g

    def visit_obj(self, obj):
        with self.g.subgraph(name=self.get_path(), graph_attr={'label': f'{self.path[-1]}={str(obj)}'}) as a:
            return a

    def visit_str(self, obj):
        with self.g.subgraph(name=self.get_path(), graph_attr={'label': f'{self.path[-1]}={obj}'}) as a:
            return a

    def visit_list(self, obj):
        with self.g.subgraph(name=self.get_path(), graph_attr={'label': self.path[-1]}) as a:
            g = self.g
            self.g = a
            res = super().visit_list(obj)
            self.g = g

            s = res[0]
            for i in res[1:]:
                a.edge(s.name, i.name)
                s = i
            return a

    def visit_dict(self, obj):
        with self.g.subgraph(name=self.get_path(), graph_attr={'label': self.path[-1]}) as a:
            g = self.g
            self.g = a
            res = super().visit_dict(obj)
            self.g = g
            return a


class PrintTableVisitor(ContextAwareVisitor):
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