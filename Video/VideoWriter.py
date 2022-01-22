import av


class VideoWriter:
    def __init__(self, path, frame_rate, bit_rate=1000000, codec='h264', pixel_format='yuv420p', profile=None
                 , channel_format='rgb24'):
        self.codec = codec
        self.channel_format = channel_format
        self.profile = profile
        self.container = av.open(path, mode='w')
        self.stream = self.container.add_stream(self.codec, rate=frame_rate)
        self.stream.pix_fmt = pixel_format
        self.stream.bit_rate = bit_rate
        if self.codec is 'prores':
            self.stream.profile = profile

    def write(self, frames):
        # frames: [T, C, H, W]
        self.stream.width = frames.size(3)
        self.stream.height = frames.size(2)
        if frames.size(1) == 1:
            frames = frames.repeat(1, 3, 1, 1)  # convert grayscale to RGB
        frames = frames.mul(255).byte().cpu().permute(0, 2, 3, 1).numpy()
        for t in range(frames.shape[0]):
            frame = frames[t]
            frame = av.VideoFrame.from_ndarray(frame, format=self.channel_format)
            self.container.mux(self.stream.encode(frame))

    def close(self):
        self.container.mux(self.stream.encode())
        self.container.close()
