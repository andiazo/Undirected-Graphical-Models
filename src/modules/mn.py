


class MarkovNetwork(nn.Module):
    def __init__(self, A, dtype, device, num_layer = 5, gamma = 0.9):
        super(MarkovNetwork, self).__init__()
        self.gamma = gamma
        self.n = A.shape[0]
        self.num_layer = num_layer
        self.dtype = dtype
        self.device = device
        
        self.A = torch.tensor(A, dtype = self.dtype, device = self.device)
        self.A = torch.clamp(self.A, min=0, max=1)
        
        self.A_list = torch.empty(self.num_layer, self.n, self.n, dtype = self.dtype, device = self.device)
        for i in range(self.num_layer):
            if i == 0:
                self.A_list[i] = self.A
            else:
                self.A_list[i] = torch.clamp(torch.matmul(self.A_list[i-1], self.A), min=0, max=1)


        W_list = torch.empty(self.num_layer, self.n, self.n, dtype = self.dtype, device = self.device)
        nn.init.uniform_(W_list)
        self.W_list = torch.nn.Parameter(W_list)
        
        
    def forward(self, input):
        batch_size = input.size(0)
        type_size = input.size(1)
        step_size = input.size(2)
        spatial_size = input.size(3)

        X = torch.squeeze(input[:,0,:,:])
        M = torch.squeeze(input[:,1,:,:])
        
        Y_hat = None
        for i in range(0, self.num_layer):
            if i == 0:
                Y_hat = self.gamma * (torch.mm(X[:,-1,:], self.A_list[0] * self.W_list[0]))
            elif i == 1:
                Y_hat += self.gamma**2 * (torch.mm(X[:,-2,:] * (1-M[:,-1,:]), self.A_list[1] * self.W_list[1]))
            else: # i >= 2
                NonMissing = (1-M[:,-1,:])
                for j in range(1, i):
                    NonMissing = NonMissing * (1-M[:,-(j+1),:])
                Y_hat += self.gamma**(i+1) * (torch.mm(X[:,-(i+1),:] * NonMissing, self.A_list[i] * self.W_list[i]))
        
        return Y_hat