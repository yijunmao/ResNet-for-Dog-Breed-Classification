# -*- coding: utf-8 -*-
"""ResNet50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IapsqqXOreViF1PU04r8dhJcuYLfAS0L
"""

import torch
import torch.nn as nn
import torchvision
import numpy as np

__all__ = ['ResNet50', 'ResNet101', 'ResNet152']

# define basic block before bottleneck blocks
def BasicBlock(in_planes, out_planes, stride=2):
  return nn.Sequential(nn.Conv2d(in_planes, out_planes, kernel_size=7, stride=stride, padding=3, bias=False), 
                       nn.BatchNorm2d(out_planes),
                       nn.ReLU(inplace=True),
                       nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

# define bottleneck blocks
class BottleNeck(nn.Module):
  def __init__(self, in_planes, out_planes, stride=1, downsampling=False, expansion=4):
    # call the constructor of parent class
    super(BottleNeck, self).__init__()
    # expansion=out/in, downsampling for addition of input with output
    self.expansion = 4
    self.downsample = downsampling
    self.relu = None
    
    # define bottleneck block
    self.bottleneck = nn.Sequential(nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=1, bias=False),
                                    nn.BatchNorm2d(out_planes),
                                    nn.ReLU(inplace=True),
                                    nn.Conv2d(out_planes, out_planes, kernel_size=3, stride=1, padding=1, bias=False),
                                    nn.BatchNorm2d(out_planes),
                                    nn.ReLU(inplace=True),
                                    nn.Conv2d(out_planes, out_planes*self.expansion, kernel_size=1, stride=1, bias=False),
                                    nn.BatchNorm2d(out_planes*self.expansion),
                                   )
    
    # downsampling the input dimensions to add with output
    if self.downsample:
      self.downsample = nn.Sequential(nn.Conv2d(in_planes, out_planes*self.expansion, kernel_size=1, stride=stride, bias=False),
                                        nn.BatchNorm2d(out_planes*self.expansion))
      self.relu = nn.ReLU(inplace=True)
  
  
  # define forward method for bottleneck class
  def forward(self, x):
    res = x
    out = self.bottleneck(x)
    
    print("out type is: ", type(out))
    
    if self.downsample:
      res = self.downsample(x)
    
    print("res type is: ", type(res))
 
    out += res
    out = self.relu(out)
    
    return out

# define ResNet class
class ResNet(nn.Module):
  def __init__(self, blocks, num_classes=133, expansion=4):
    super(ResNet, self).__init__()
    
    self.expansion = expansion
    
    # call the basic block before bottleneck blocks
    self.basicblock = BasicBlock(in_planes=3, out_planes=64)
    
    # define 4 subsequent layers consisting of bottleneck blocks
    self.layer1 = self.make_layer(in_planes=64, out_planes=64, block=blocks[0], stride=1)
    self.layer2 = self.make_layer(in_planes=256, out_planes=128, block=blocks[1], stride=2)
    self.layer3 = self.make_layer(in_planes=512, out_planes=256, block=blocks[2], stride=2)
    self.layer4 = self.make_layer(in_planes=1024, out_planes=512, block=blocks[3], stride=2)
    
    # define average pooling layer and fully connected layer before bottleneck blocks
    self.avgpool = nn.AvgPool2d(7, stride=1)
    self.fc = nn.Linear(2048, num_classes)
    
    # initialize convolution, bn, weight, and bias
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
      elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias, 0)
    
  # define the make layer function
  def make_layer(self, in_planes, out_planes, block, stride):
    layers = []
    # make the first layer of each bottleneck block type
    # input and output feature map dimensions are given
    layers.append(BottleNeck(in_planes, out_planes, stride, downsampling=True))
    
    # make the rest layers of each bottleneck block type
    # input feature map dimensions is four times that of output feature map
    for i in range(1, block):
      layers.append(BottleNeck(out_planes*self.expansion, out_planes))
    
    return nn.Sequential(*layers)
  
  # define forward method for ResNet class
  def forward(self, x):
    x = self.basicblock(x)
    
    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.layer4(x)
    
    x = self.avgpool(x)
    x = out.view(out.size(0), -1)
    x = self.fc(x)
    
    return x

# define different types of ResNets including ResNet50, ResNet101, and ResNet152
def ResNet50():
  return ResNet([3, 4, 6, 3])

def ResNet101():
  return ResNet([3, 4, 23, 3])

def ResNet152():
  return ResNet([3, 8, 36, 3])

# main function to test different resnets
model = ResNet50()
print(model)

'''
import torchvision.models as models
resnet50 = models.resnet50()
print(resnet50)
'''

