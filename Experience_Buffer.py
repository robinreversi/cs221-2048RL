import random
class Experience_Buffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size



    def add(self, experience):
        '''
        experience should be a tuple consisting of (state, action, reward, new_state)
        '''
        if(len(self.buffer) + 1 > self.size):
            self.buffer.pop(0)
        self.buffer.append(experience)

    def sample(self, sample_size):
        '''
        randomly sample sample_size experiences from the buffer
        '''
        return random.sample(self.buffer, sample_size)