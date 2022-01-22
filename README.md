# Description

A PyTorchMediaIO object to help in importing and exporting Images and Videos as Pytorch Datasets.

# Requirements

- pims  
- numpy 
- Pytorch  
- torchvision
- PIL

User can install from requirements.txt

# Usage

## Open File

```python
import os
from torchvision.transforms import ToTensor
from PyTorchMediaIO import PyTorchMediaIO


def TestMediaLoader():
    testMediaMp4 = "testMedia/seq1.mp4"
    testMediaMov = "testMedia/seq1.mov"
    testMediaImg = "testMedia/seq1/img/seq1.png"
    exists = os.path.exists(testMediaMp4)
    mediaLoader = PyTorchMediaIO()
    mediaLoader.Open(path=testMediaMov, transform=ToTensor())
    size = mediaLoader.GetDimensions()
    FrameCount = mediaLoader.GetFrameCount()
    MediaType = mediaLoader.GetMediaType()
    DataloaderFiles = mediaLoader.GetDataloaderFiles()
    Duration = mediaLoader.GetDuration()
```

## Get Frames as Pytorch Dataset and Tensors

```python
mediaLoader = MediaIO()
mediaLoader.Open(path=testMediaMov, transform=ToTensor())
mediaLoader.GetDataloaderFiles()  # RGB tensor normalized to 0 ~ 1.
```

## Save to Video / Prores

```python

mediaLoader = MediaIO()
mediaLoader.Open(path=testMediaMov, transform=ToTensor())
mediaLoader.GetDataloaderFiles()  # RGB tensor normalized to 0 ~ 1.

outputPath = "C:/temp/tempfile_prores.mov"
ExportProresVideo(outputPath ,mediaLoader.frame_rate, DataloaderFiles)


def ExportProresVideo(OutputPath,FrameRate,DataloaderFiles):
    # Export Prores Video
    mediaExporter = MediaIO(path=OutputPath, frame_rate=FrameRate, bit_rate=50000,
                            codec='prores', pixel_format='yuv422p10le', profile=3)

    mediaExporterWriter = mediaExporter.Writer()
    for src in DataloaderFiles:
        mediaExporterWriter.write(src)
    mediaExporterWriter.close()
```
