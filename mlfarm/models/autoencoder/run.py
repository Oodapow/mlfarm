import importlib
import yaml
import os
import pytorch_lightning as pl

with open(os.path.abspath(os.path.join(__file__, '..', 'config.yml')), 'r') as f:
    data = yaml.safe_load(f)

class NotSupported(Exception):
    pass

class ClassBuilder:
    def __init__(self, class_name, module_name, args):
        self._class = getattr(importlib.import_module(module_name), class_name)
        self.args = args
    
    def __call__(self, args=None):
        if (not self.args) and args:
            self.args = args
        elif self.args and args:
            if isinstance(self.args, dict) and isinstance(args, dict):
                self.args.update(args)
            else:
                raise NotSupported('Builder with args work only with dicts.')

        if not self.args:
            obj = self._class()
        elif isinstance(self.args, list):
            obj = self._class(*self.args)
        elif isinstance(self.args, dict):
            obj = self._class(**self.args)
        else:
            obj = self._class(self.args)
        return obj

def build_class(d):
    if isinstance(d, dict):
        if 'class' in d:
            d = d.copy()
            if 'args' in d:
                d['args'] = build_class(d['args'])
            split = d['class'].split('.')
            builder = ClassBuilder(split[-1], '.'.join(split[:-1]), d.get('args', None))
            if d.get('builder', False):
                return builder
            else:
                return builder()
        else:
            res = {}
            for k,v in d.items():
                res[k] = build_class(v)
            return res
    elif isinstance(d, list):
        return [build_class(i) for i in d]
    else:
        return d

module = build_class(data)
module.hparams = data
print(module)
trainer = pl.Trainer()
trainer.fit(module)