import yaml
import os
import pytorch_lightning as pl
import mlfarm.core

with open(os.path.abspath(os.path.join(__file__, '..', 'config.yml')), 'r') as f:
    data = yaml.safe_load(f)


cv = mlfarm.core.ClassVisitor()

module = cv.visit(data)
module.hparams = data
print(module)
trainer = pl.Trainer()
trainer.fit(module)