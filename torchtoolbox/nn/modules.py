#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author：X.Yang(xuyang@deepmotion.ai)

from . import functional as F
from torch import nn


class ChannelShuffle(nn.Module):
    def __init__(self, groups: int):
        super().__init__()
        self.groups = groups

    def forward(self, x):
        x = F.channel_shuffle(x, self.groups)
        return x


class ChannelCircularShift(nn.Module):
    def __init__(self, num_shift):
        super().__init__()
        self.shift = num_shift

    def forward(self, x):
        return F.channel_shift(x, self.shift)
