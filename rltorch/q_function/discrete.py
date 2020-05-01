from rltorch.network import BaseNetwork, create_dqn_base,\
    create_linear_network


class DiscreteConvQNetwork(BaseNetwork):
    def __init__(self, num_channels, output_dim, initializer='xavier'):
        super(DiscreteConvQNetwork, self).__init__()

        self.base = create_dqn_base(num_channels, initializer=initializer)
        self.V_stream = create_linear_network(
            7*7*64, 1, hidden_units=[512], initializer=initializer)
        self.A_stream = create_linear_network(
            7*7*64, output_dim, hidden_units=[512], initializer=initializer)

    def forward(self, states):
        h = self.base(states.clone())
        V = self.V_stream(h.clone())
        A = self.A_stream(h.clone())
        Q = V.clone() + A.clone() - A.clone().mean(1, keepdim=True)
        return Q


class TwinedDiscreteConvQNetwork(BaseNetwork):
    def __init__(self, num_channels, output_dim, initializer='xavier'):
        super(TwinedDiscreteConvQNetwork, self).__init__()

        self.Q1 = DiscreteConvQNetwork(
            num_channels, output_dim, initializer)
        self.Q2 = DiscreteConvQNetwork(
            num_channels, output_dim, initializer)

    def forward(self, states):

        Q2 = self.Q2(states.clone())
        Q1 = self.Q1(states.clone())
        return Q1, Q1
