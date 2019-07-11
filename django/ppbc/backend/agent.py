class agent(object):
    """"""
    def __init__(self, it, ot, seed, key, name, wallet_name):
        """
        initializes the aries agent
        :param it: inbound transport. The port the agent listens to for incoming data
        :type it: int
        :param ot: outbound transport. The port the agent sends data on, The API is on this port
        :type ot: int
        :param seed: a unique 32 byte string of numbers used to genereate the wallet
        :type seed: str
        :param key: used to unlock the agent wallet
        :type key: int
        :param name: the name of the agent
        :type name: str
        :param wallet_name: the label for the agent wallet
        :type wallet_name: str
        """
        self.it = it
        self.ot = ot
        self.seed = seed
        self.key = key
        self.name = name
        self.wallet_name = wallet_name

    def start_agent():
        

if __name__ == '__main__':
    alice = agent(10000, 5000, '00000000000000000000000000000000', 'key', 'alice', 'alice_w')
    print("hello from main!")
