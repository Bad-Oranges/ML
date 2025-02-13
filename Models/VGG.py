import torch
import torch.nn as nn
from Basic_Conv import BasicConv


class VGG(nn.Module):
    def __init__(self, class_num=100):
        super(VGG, self).__init__()

        cfg = [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M']
        layers = []
        in_channels = 3
        for v in cfg:
            if v == 'M':
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            # CBR
            else:
                layers.append(BasicConv(in_channels, v, 3, padding=1, bn=True, activate=True))
                in_channels = v

        self.features = nn.Sequential(*layers)
        self.avgPool = nn.AdaptiveAvgPool2d(7)
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, class_num)
        )

        # model init
        for m in self.modules():
            match m:
                case nn.Conv2d:
                    nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                    if m.bias is not None:
                        nn.init.constant_(m.bias, 0)
                case nn.BatchNorm2d:
                    nn.init.constant_(m.weight, 1)
                    nn.init.constant_(m.bias, 1)
                case nn.Linear:
                    nn.init.normal_(m.weight, 0, 0.01)
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = self.avgPool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)

        return x



if __name__ == '__main__':
    x = torch.randn(20, 3, 400, 400)
    model = VGG
    out = model(x)

