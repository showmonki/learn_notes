import torch
import torch.nn as nn
from torchsummary import summary


class BasicConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size,stride=(1,1), padding=(0,0)):
        super(BasicConv, self).__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,stride=stride, padding=padding)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.relu(x)
        return x


class InceptionBlock(nn.Module):
    def __init__(self, in_channels, ch1x1, ch3x3reduce, ch3x3, ch5x5reduce, ch5x5,chpool):
        super(InceptionBlock, self).__init__()
        self.branch1 = BasicConv(in_channels=in_channels, out_channels=ch1x1, kernel_size=1)
        self.branch2 = nn.Sequential(
            BasicConv(in_channels=in_channels, out_channels=ch3x3reduce, kernel_size=1),
            BasicConv(in_channels=ch3x3reduce, out_channels=ch3x3, kernel_size=3, padding=1)  # 3x3 padding1
        )
        self.branch3 = nn.Sequential(
            BasicConv(in_channels=in_channels, out_channels=ch5x5reduce, kernel_size=1),
            BasicConv(in_channels=ch5x5reduce, out_channels=ch5x5, kernel_size=5, padding=2)  # 5x5 padding2
        )
        self.branch4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3,stride=1,padding=1,ceil_mode=True),  # 教程中这里后面加其他参数，但之前为什么不匹配，因为默认参数么 TODO
            BasicConv(in_channels=in_channels, out_channels=chpool, kernel_size=1)
        )

    def forward(self, x):
        x1 = self.branch1(x)
        x2 = self.branch2(x)
        x3 = self.branch3(x)
        x4 = self.branch4(x)
        x = torch.cat([x1, x2, x3, x4], dim=1)
        return x


class InceptionV1(nn.Module):
    def __init__(self, num_classes):
        super(InceptionV1, self).__init__()
        self.BasicConv1 = BasicConv(in_channels=3, out_channels=64, kernel_size=7,stride=2, padding=3)
        self.max_pool1 = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)
        # self.BasicConv2 = BasicConv(in_channels=64, out_channels=192, kernel_size=3,stride=1)
        self.conv1x1 = BasicConv(in_channels=64, out_channels=64, kernel_size=1)
        self.conv3x3 = BasicConv(in_channels=64, out_channels=192, kernel_size=3, padding=1)
        self.max_pool2 = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)

        self.InceptionBlock_3a = InceptionBlock(192,64,96,128,16,32,32)
        self.InceptionBlock_3b = InceptionBlock(256,128,128,192,32,96,64)

        self.max_pool3 = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)

        self.InceptionBlock_4a = InceptionBlock(480, 192, 96, 208, 16, 48, 64)
        self.InceptionBlock_4b = InceptionBlock(512, 160, 112, 224, 24, 64, 64)
        self.InceptionBlock_4c = InceptionBlock(512, 128, 128, 256, 24, 64, 64)
        self.InceptionBlock_4d = InceptionBlock(512, 112, 144, 288, 32, 64, 64)
        self.InceptionBlock_4e = InceptionBlock(528, 256, 160, 320, 32, 128, 128)

        self.max_pool4 = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)

        self.InceptionBlock_5a = InceptionBlock(832, 256, 160, 320, 32, 128, 128)
        self.InceptionBlock_5b = InceptionBlock(832, 384, 192, 384, 48, 128, 128)

        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(in_features=1024, out_features=num_classes)

    def forward(self, x):
        x = self.BasicConv1(x)
        x = self.max_pool1(x)
        # x = self.BasicConv2(x)

        x = self.conv1x1(x)
        x = self.conv3x3(x)
        x = self.max_pool2(x)

        x = self.InceptionBlock_3a(x)
        x = self.InceptionBlock_3b(x)

        x = self.max_pool3(x)
        x = self.InceptionBlock_4a(x)
        x = self.InceptionBlock_4b(x)
        x = self.InceptionBlock_4c(x)
        x = self.InceptionBlock_4d(x)
        x = self.InceptionBlock_4e(x)
        x = self.max_pool4(x)
        x = self.InceptionBlock_5a(x)
        x = self.InceptionBlock_5b(x)

        x = self.avg_pool(x)
        x = self.flatten(x)
        x = torch.dropout(x, 0.4, train=True)
        x = self.fc(x)
        x = torch.softmax(x, dim=1)
        return x


if __name__ == '__main__':
    input = torch.ones([10, 3, 224, 224])

    model = InceptionV1(num_classes=20)

    result = model(input)

    print(result.shape)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    summary(model.to(device),(3,224,224))
    print(model)
