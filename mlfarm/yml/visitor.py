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