import os
from torchvision.transforms.functional import to_pil_image
import av
import imageio
import numpy as np
from PIL import Image


class ImageSequenceWriter:
    def __init__(self, path, extension='jpg'):
        self.filesSaved = []
        self.currentFrameName = ''
        self.currentframe = 0
        self.frames = None

        if "." + extension.lower() in path:
            try:
                self.path = os.path.splitext(path)[0]
            except:
                self.path = path
        else:
            self.path = path
        self.baseName = os.path.basename(self.path)
        self.extension = extension
        self.counter = 0
        os.makedirs(path, exist_ok=True)

    def write(self, frames):
        # frames: [T, C, H, W]
        self.frames = frames
        if 'EXR' in self.extension.upper():
            self.frames = self.frames.mul(255).byte().cpu().permute(0, 2, 3, 1).numpy()
        for t in range(frames.shape[0]):
            self.currentframe = t
            self.currentFrameName = self.path + str(self.counter).zfill(4) + '.' + self.extension

            self.filesSaved.append(self.currentFrameName)

            if 'EXR' in self.extension.upper():
                self.saveEXR()
            else:
                to_pil_image(frames[self.currentframe]).save(self.currentFrameName)
            self.counter += 1

    # #2DO
    def saveEXR(self):
        pilImage = to_pil_image(self.frames[self.currentframe], mode='RGB')
        # img = Image.fromarray((255 * pilImage[0]).numpy().astype("float32").transpose(1, 2, 0))
        # freeimage lib only supports float32 not float64 arrays
        arr = np.array(pilImage).astype("float32")

        # Write to disk
        imageio.imwrite(self.currentFrameName, arr)

    def close(self):
        pass
