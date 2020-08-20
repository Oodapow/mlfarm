import os
import re
import yaml

from mlfarm.yml.visitor import BaseVisitor


class Transform(BaseVisitor):
    def __call__(self, data):
        return self.visit(data)

class CompositeTransform(Transform):
    def __init__(self, *args):
        self.transforms = args
    
    def __call__(self, data):
        for t in self.transforms:
            data = t(data)
        return data

class FileTransform(Transform):
    def __call__(self, file_path):
        with open(file_path, 'r') as f:
            data = yaml.load(f)
        
        self.file_path = file_path
        res = self.visit(data)
        self.file_path = None
        return res

class StringParserTransform(Transform):
    def __init__(self):
        self.checker = re.compile(r'{{.*}}')
    
    def pre_process(self):
        pass

    def process(self, obj):
        return obj

    def post_process(self, data):
        pass

    def visit_str(self, obj):
        ch = obj.strip()
        if self.checker.fullmatch(ch):
            self.pre_process()
            data = self.process(ch[2:-2].strip())
            try:
                res = self(data)
            except:
                return obj
            self.post_process(data)
            return res
        return obj


class TemplateTransform(StringParserTransform):
    def __init__(self, template_data):
        super().__init__()
        self.template_data = template_data
    
    def process(self, obj):
        fp = os.path.abspath(os.path.join(self.file_path, '..', obj))
        return fp


class RelativeLoadTransform(FileTransform, StringParserTransform):
    def pre_process(self):
        self.last_file_path = self.file_path

    def process(self, obj):
        fp = os.path.abspath(os.path.join(self.file_path, '..', obj))
        return fp

    def post_process(self, obj):
        self.file_path = self.last_file_path