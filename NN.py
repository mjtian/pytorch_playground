import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5) #(nsanples*nchannels*height*width)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return (x)

    def num_flat_feature(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *=s
        return num_features

net = Net()
print (net)

params = list(net.parameters())
print (len(params))
print (params[0].size) #conv1 .weight

input = torch.randn(1 , 1, 32, 32) #bach size,color channel，w，h
out = net(input)
target = torch.randn(10)
target = target.view(1, -1)
criterion = nn.MSELoss()
loss = criterion(out, target)
print (loss)
print (out)

net.zero_grad()
out.backward(torch.randn(1, 10))

# the whole follow:
# input -> conv2d -> relu -> maxpool2d ->
# conv2d -> relu -> maxpool2d ->
# view -> linear -> lelu -> linear -> relu -> linear
# MSELoss ->
# loss

print (loss.grad_fn) #MSELoss
print (loss.grad_fn.next_functions[0][0]) #Linear
print (loss.grad_fn.next_functions[0][0].next_functions[0][0]) #Relu





