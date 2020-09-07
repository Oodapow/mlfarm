from mlfarm.visitors.core import BaseVisitor

import yaml
import os

class YMLLoadVisitor(BaseVisitor):
    def visit_str(self, obj):
        if os.path.isfile(obj) and (obj.endswith('.yml') or obj.endswith('.yaml')):
            with open(obj, 'r') as f:
                return yaml.safe_load(f)
        return obj
