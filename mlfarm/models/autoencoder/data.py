import torch
import json
import os
from PIL import Image, ImageOps

class ImagesDataset(torch.utils.data.Dataset):
    def __init__(self, root, loader, transform=None):
        super(ImagesDataset, self).__init__()

        self.root = root
        self.transform = transform
        self.loader = loader

        with open(os.path.join(root, 'md5.json'), 'r') as f:
            self.filenames = [x[0] for x in json.load(f).values()]

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, i):
        out = self.loader(self.filenames[i])
        if self.transform:
            out = self.transform(out)
            return { 'filename': self.filenames[i], 'image': out }
        return { 'filename': self.filenames[i], 'image': out }


class PILImageLoader:
    def __init__(self, mode='RGB'):
        self.mode = mode

    def __call__(self, x):
        with open(x, 'rb') as f:
            img = Image.open(f)
            return img.convert(self.mode)