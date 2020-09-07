from mlfarm.visitors.core import BaseVisitor

import re
import os

class StringValueVisitor(BaseVisitor):
    checker = re.compile(r'{{.*}}')
    
    def process(self, ch):
        return ch

    def visit_str(self, obj):
        ch = obj.strip()
        if self.checker.fullmatch(ch):
            ch = ch[2:-2].strip()
            return self.process(ch)
        return obj

class RelativeFileVisitor(StringValueVisitor):
    word = r'relative:'
    p_checker = re.compile(word + r'.*')

    def __init__(self, file):
        self.file = file
    
    def process(self, ch):
        if self.p_checker.fullmatch(ch):
            ch = ch[len(self.word):].strip()
            ch = os.path.abspath(os.path.join(self.file, '..', ch))
        return ch

class VariablesVisitor(StringValueVisitor):
    word = r'relative:'
    p_checker = re.compile(word + r'.*')

    def __init__(self, file):
        self.file = file
    
    def process(self, ch):
        if self.p_checker.fullmatch(ch):
            ch = ch[len(self.word):].strip()
            ch = os.path.abspath(os.path.join(self.file, '..', ch))
        return ch