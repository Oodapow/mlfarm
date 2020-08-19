import torch
from torch import nn

class ResBlock(nn.Module):
    def __init__(self, seq, act, trm):
        super().__init__()
        self.seq = seq
        self.trm = trm
        self.act = act
    
    def forward(self, x):
        res = self.act(self.seq(x) + self.trm(x))
        return res


class RepeaterBlock(nn.Sequential):
    def __init__(self, block_builder, times):
        super().__init__(*[block_builder() for _ in range(times)])


class Conv2d3x3ReLuResBlock(ResBlock):
    def __init__(self, ch_in, ch_mid, ch_out):
        super().__init__(
            nn.Sequential(
                nn.Conv2d(ch_in, ch_mid, 3, bias=False, padding=1),
                nn.ReLU(),
                nn.Conv2d(ch_mid, ch_out, 3, bias=False, padding=1)
            ),
            nn.ReLU(),
            nn.Identity() if ch_in == ch_out else nn.Conv2d(ch_in, ch_out, 1)
        )


class Conv2d3x3ReLuMaxPoolResBlock(ResBlock):
    def __init__(self, ch_in, ch_mid, ch_out, stride):
        super().__init__(
            nn.Sequential(
                nn.Conv2d(ch_in, ch_mid, 3, bias=False, padding=1, stride=stride),
                nn.ReLU(),
                nn.Conv2d(ch_mid, ch_out, 3, bias=False, padding=1)
            ),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=stride) if ch_in == ch_out else nn.Sequential(nn.MaxPool2d(2, stride=stride), nn.Conv2d(ch_in, ch_out, 1))
        )