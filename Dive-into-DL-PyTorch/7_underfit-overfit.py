import torch
import torch.utils.data as Data
import numpy as np 
import d2lzh_pytorch as d2l

n_train, n_test, true_w, true_b = 100, 100, [1.2, -3.4, 5.6], 5
features = torch.randn(n_test + n_train, 1)

poly_features = torch.cat((features, torch.pow(features, 2), torch.pow(features, 3)), 1)
labels = true_w[0] * poly_features[:, 0] + true_w[1] * poly_features[:, 1] + true_w[2] * poly_features[:, 2] + true_b
labels += torch.tensor(np.random.normal(0, 0.01, size=labels.size()), dtype=torch.float)


num_epochs = 100
loss = torch.nn.MSELoss()

def fit_and_plot(train_features, test_features, train_lables, test_lables):
    net = torch.nn.Linear(train_features.shape[-1], 1)

    batch_size = min(10, train_lables.shape[0])
    dataset = Data.TensorDataset(train_features, train_lables)
    train_iter = Data.DataLoader(dataset, batch_size, shuffle=True)

    optimizer = torch.optim.SGD(net.parameters(), lr = 0.01)

    train_ls, test_ls = [], []

    for _ in range(num_epochs):
        for x, y in train_iter:
            l = loss(net(x), y.view(-1, 1))
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
        train_lables =  train_lables.view(-1, 1)
        test_lables = test_lables.view(-1, 1)
        train_ls.append(loss(net(train_features), train_lables).item())
        test_ls.append(loss(net(test_features), test_lables).item())
    
    print('final epoch: train loss', train_ls[-1], 'test loss', test_ls[-1])
    d2l.semilogy(range(1, num_epochs + 1), train_ls, 'epochs', 'loss',
                range(1, num_epochs + 1,), test_ls, ['train', 'test'])
    print('weight:', net.weight.data, '\nbias:', net.bias.data)
#正常
fit_and_plot(poly_features[:n_train, :], poly_features[n_train:, :], labels[:n_train], labels[n_train:])
#欠拟合
fit_and_plot(features[:n_train, :], features[n_train:, :], labels[:n_train], labels[n_train:])
#过拟合
fit_and_plot(poly_features[0:2, :], poly_features[n_train:, :], labels[0:2], labels[n_train:])