import os

import pims
import numpy as np
from torch.utils.data import Dataset
from PIL import Image


class ImageSequenceReader(Dataset):
    def __init__(self, path, transform=None):
        self.shape = None
        self.path = path
        try:
            self.files = sorted(os.listdir(self.path))
        except:
            self.path = os.path.dirname(self.path)
            self.files = sorted(os.listdir(self.path))
        self.transform = transform
        self.getShape()

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        with Image.open(os.path.join(self.path, self.files[idx])) as img:
            img.load()
        if self.transform is not None:
            return self.transform(img)
        return img

    def getShape(self):
        frame = None
        with Image.open(os.path.join(self.path, self.files[0])) as frame:
            frame.load()
        img = np.array(frame)
        self.shape = img.shape[-1]
        return self.shape

    def getFrameNonTransformed(self, idx):
        with Image.open(os.path.join(self.path, self.files[idx])) as img:
            img.load()
        return img

    def asNumpyArray(self):
        npar = []
        for frameName in self.files:
            frame = None
            with Image.open(os.path.join(self.path, frameName)) as frame:
                frame.load()
            npar.append(np.array(frame))
        return npar
