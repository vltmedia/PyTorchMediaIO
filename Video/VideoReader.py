import pims
import numpy as np
from torch.utils.data import Dataset
from PIL import Image


class VideoReader(Dataset):
    def __init__(self, path, transform=None):
        self.shape = None
        self.video = pims.PyAVVideoReader(path)
        self.rate = self.video.frame_rate
        self.transform = transform
        self.getShape()

    @property
    def frame_rate(self):
        return self.rate

    def getShape(self):
        frame = self.video[0]
        img = np.array(frame)
        self.shape = img.shape[-1]
        return self.shape

    def asNumpyArray(self):
        return [np.array(frame) for frame in self.video]



    def __len__(self):
        return len(self.video)

    def __getitem__(self, idx):
        frame = self.video[idx]
        frame = Image.fromarray(np.asarray(frame))
        if self.transform is not None:
            frame = self.transform(frame)
        return frame

    def getFrameNonTransformed(self, idx):
        frame = self.video[idx]
        frame = Image.fromarray(np.asarray(frame))
        return frame
