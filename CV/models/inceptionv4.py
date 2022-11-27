import torch
import torch.nn as nn


class BasicConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size,stride=(1,1), padding=(0,0)):
        super(BasicConv, self).__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,stride=stride, padding=padding)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class StemModel(nn.Module):
    def __init__(self):
        super(StemModel, self).__init__()
        self.conv1 = BasicConv(in_channels=3, out_channels=32, kernel_size=3, stride=2)
        self.conv2 = BasicConv(in_channels=32, out_channels=32, kernel_size=3)
        self.conv3 = BasicConv(in_channels=32, out_channels=64, kernel_size=3, padding=1)

        self.branch1_1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.branch1_2 = BasicConv(in_channels=64, out_channels=96, kernel_size=3, stride=2)

        self.branch2_1 = nn.Sequential(
            BasicConv(in_channels=160, out_channels=64, kernel_size=1),
            BasicConv(in_channels=64,out_channels=96,kernel_size=3)
        )
        self.branch2_2 = nn.Sequential(
            BasicConv(in_channels=160, out_channels=64, kernel_size=1),
            BasicConv(in_channels=64,out_channels=64,kernel_size=(7,1), padding=(3,0)),
            BasicConv(in_channels=64,out_channels=64,kernel_size=(1,7), padding=(0,3)),
            BasicConv(in_channels=64, out_channels=96, kernel_size=3)
        )
        self.branch3_1 = BasicConv(in_channels=192, out_channels=192, kernel_size=3,stride=2)
        self.branch3_2 = nn.MaxPool2d(kernel_size=3, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x1_1 = self.branch1_1(x)
        x1_2 = self.branch1_2(x)
        x = torch.cat([x1_1,x1_2],dim=1)

        x2_1 = self.branch2_1(x)
        x2_2 = self.branch2_2(x)
        x = torch.cat([x2_1, x2_2], dim=1)

        x3_1 = self.branch3_1(x)
        x3_2 = self.branch3_2(x)
        x = torch.cat([x3_1,x3_2], dim=1)
        return x


class InceptionAModel(nn.Module):
    def __init__(self):
        super(InceptionAModel, self).__init__()
        self.branch_1 = nn.Sequential(
            nn.AdaptiveAvgPool2d((35)),
            BasicConv(in_channels=384, out_channels=96,kernel_size=1)
        )
        self.branch_2 = BasicConv(in_channels=384, out_channels=96, kernel_size=1)
        self.branch_3 = nn.Sequential(
            BasicConv(in_channels=384, out_channels=64, kernel_size=1),
            BasicConv(in_channels=64, out_channels=96, kernel_size=3, padding=1)
        )
        self.branch_4 = nn.Sequential(
            BasicConv(in_channels=384, out_channels=64, kernel_size=1),
            BasicConv(in_channels=64, out_channels=96, kernel_size=3, padding=1),
            BasicConv(in_channels=96, out_channels=96, kernel_size=3, padding=1)
        )

    def forward(self, x):
        x1 = self.branch_1(x)
        x2 = self.branch_2(x)
        x3 = self.branch_3(x)
        x4 = self.branch_4(x)
        x = torch.cat([x1, x2, x3, x4], dim=1)
        return x


class InceptionBModel(nn.Module):
    def __init__(self):
        super(InceptionBModel, self).__init__()
        self.branch_1 = nn.Sequential(
            nn.AdaptiveAvgPool2d((17)),
            BasicConv(in_channels=1024, out_channels=128, kernel_size=1)
        )
        self.branch_2 = BasicConv(in_channels=1024, out_channels=384, kernel_size=1)
        self.branch_3 = nn.Sequential(
            BasicConv(in_channels=1024, out_channels=192, kernel_size=1),
            BasicConv(in_channels=192, out_channels=224, kernel_size=(1, 7), padding=(0, 3)),
            BasicConv(in_channels=224, out_channels=256, kernel_size=(1, 7), padding=(0, 3))
        )
        self.branch_4 = nn.Sequential(
            BasicConv(in_channels=1024, out_channels=192, kernel_size=1),
            BasicConv(in_channels=192, out_channels=192, kernel_size=(1, 7), padding=(0, 3)),
            BasicConv(in_channels=192, out_channels=224, kernel_size=(7, 1), padding=(3, 0)),
            BasicConv(in_channels=224, out_channels=224, kernel_size=(1, 7), padding=(0, 3)),
            BasicConv(in_channels=224, out_channels=256, kernel_size=(7, 1), padding=(3, 0))
        )

    def forward(self, x):
        x1 = self.branch_1(x)
        x2 = self.branch_2(x)
        x3 = self.branch_3(x)
        x4 = self.branch_4(x)
        x = torch.cat([x1, x2, x3, x4], dim=1)
        return x


class InceptionCModel(nn.Module):
    def __init__(self):
        super(InceptionCModel, self).__init__()
        self.branch_1 = nn.Sequential(
            nn.AdaptiveAvgPool2d((8)),
            BasicConv(in_channels=1536, out_channels=256, kernel_size=1)
        )
        self.branch_2 = BasicConv(in_channels=1536, out_channels=256, kernel_size=1)
        self.branch_3_1 = BasicConv(in_channels=1536, out_channels=384, kernel_size=1)
        self.branch_3a = BasicConv(in_channels=384, out_channels=256, kernel_size=(1, 3), padding=(0, 1))
        self.branch_3b = BasicConv(in_channels=384, out_channels=256, kernel_size=(3, 1), padding=(1, 0))
        self.branch_4 = nn.Sequential(
            BasicConv(in_channels=1536, out_channels=384, kernel_size=1),
            BasicConv(in_channels=384, out_channels=448, kernel_size=(1, 3), padding=(0, 1)),
            BasicConv(in_channels=448, out_channels=512, kernel_size=(3, 1), padding=(1, 0))
        )
        self.branch_4a = BasicConv(in_channels=512, out_channels=256, kernel_size=(1, 3), padding=(0, 1))
        self.branch_4b = BasicConv(in_channels=512, out_channels=256, kernel_size=(3, 1), padding=(1, 0))

    def forward(self, x):
        x1 = self.branch_1(x)
        x2 = self.branch_2(x)
        x3_1 = self.branch_3_1(x)
        x3a = self.branch_3a(x3_1)
        x3b = self.branch_3b(x3_1)
        x4 = self.branch_4(x)
        x4a = self.branch_4a(x4)
        x4b = self.branch_4b(x4)
        x = torch.cat([x1, x2, x3a,x3b, x4a,x4b], dim=1)
        return x


class ReductionA(nn.Module):
    def __init__(self):
        super(ReductionA, self).__init__()
        self.branch_1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.branch_2 = BasicConv(in_channels=384, out_channels=384, kernel_size=3, stride=2)
        self.branch_3 = nn.Sequential(
            BasicConv(in_channels=384, out_channels=192, kernel_size=1),
            BasicConv(in_channels=192, out_channels=224, kernel_size=3),
            BasicConv(in_channels=224, out_channels=256, kernel_size=3, stride=2,padding=1)
        )

    def forward(self, x):
        x1 = self.branch_1(x)
        x2 = self.branch_2(x)
        x3 = self.branch_3(x)
        x = torch.cat([x1, x2, x3], dim=1)
        return x


class ReductionB(nn.Module):
    def __init__(self):
        super(ReductionB, self).__init__()
        self.branch_1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.branch_2 = nn.Sequential(
            BasicConv(in_channels=1024, out_channels=192, kernel_size=1),
            BasicConv(in_channels=192, out_channels=192, kernel_size=3, stride=2)
        )
        self.branch_3 = nn.Sequential(
            BasicConv(in_channels=1024, out_channels=256, kernel_size=1),
            BasicConv(in_channels=256, out_channels=320, kernel_size=(1,7), padding=(0,3)),
            BasicConv(in_channels=320, out_channels=320, kernel_size=(7,1), padding=(3,0)),
            BasicConv(in_channels=320, out_channels=320, kernel_size=3, stride=2)
        )

    def forward(self, x):
        x1 = self.branch_1(x)
        x2 = self.branch_2(x)
        x3 = self.branch_3(x)
        x = torch.cat([x1, x2, x3], dim=1)
        return x


class InceptionV4(nn.Module):
    def __init__(self, num_classes):
        super(InceptionV4, self).__init__()
        self.stem = StemModel()
        self.modelA1 = InceptionAModel()
        self.modelA2 = InceptionAModel()
        self.modelA3 = InceptionAModel()
        self.modelA4 = InceptionAModel()
        self.reductionA = ReductionA()
        self.modelB1 = InceptionBModel()
        self.modelB2 = InceptionBModel()
        self.modelB3 = InceptionBModel()
        self.modelB4 = InceptionBModel()
        self.modelB5 = InceptionBModel()
        self.modelB6 = InceptionBModel()
        self.modelB7 = InceptionBModel()
        self.reductionB = ReductionB()
        self.modelC1 = InceptionCModel()
        self.modelC2 = InceptionCModel()
        self.modelC3 = InceptionCModel()
        self.avgpool = nn.AdaptiveAvgPool2d((1))
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(in_features=1536, out_features=num_classes)

    def forward(self, x):
        x = self.stem(x)
        x = self.modelA1(x)
        x = self.modelA2(x)
        x = self.modelA3(x)
        x = self.modelA4(x)
        x = self.reductionA(x)
        x = self.modelB1(x)
        x = self.modelB2(x)
        x = self.modelB3(x)
        x = self.modelB4(x)
        x = self.modelB5(x)
        x = self.modelB6(x)
        x = self.modelB7(x)
        x = self.reductionB(x)
        x = self.modelC1(x)
        x = self.modelC2(x)
        x = self.modelC3(x)
        x = self.avgpool(x)
        x = self.flatten(x)

        x = torch.dropout(x, 0.2, train=True)
        x = self.fc(x)
        x = torch.softmax(x, dim=1)

        return x


if __name__ == '__main__':
    input = torch.ones([20,3,299,299])
    
    model = InceptionV4(num_classes=5)
    
    output = model(input)
    
    print(output.shape)
