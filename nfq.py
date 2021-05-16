from RobotHoop import RobotHoop
import random, time
import numpy as np
import matplotlib.pyplot as plt
import torch

iterations = 200
maxsteps = 100
epochs = 50


allactions = [('f', 'f', False), ('f', 's', False), ('f', '', False), ('s', 'f', False), ('s', 's', False), ('s', '', False), ('', 'f', False), ('', 's', False), ('','',False), ('', '', True)]

class NeuralNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = torch.nn.Sequential(torch.nn.Linear(5, 10), torch.nn.Linear(10, 1))
    def forward(self, x):
        return self.layers(x)



states = []
actions = []
rewards = []
next_states = []
for i in range(iterations):
    env = RobotHoop(-2,.5,.5, False)
    for j in range(maxsteps):
        state = env.state()
        action = random.choice(allactions)
        ac_num = allactions.index(action)
        res = env.step(*action)
        reward = res['reward']
        states.append(state)
        actions.append(ac_num)
        rewards.append(reward)
        next_states.append(env.state())
        if res['end']:
            break


discount_factor = .95

Q= NeuralNet()
optimizer = torch.optim.Rprop(Q.parameters())
for i in range(epochs):
    Q= NeuralNet()
    print(i)
    for j in range(len(states)):
        st = torch.tensor(states[j]).float()
        ac = torch.tensor(actions[j]).float()
        re = torch.tensor(rewards[j]).float()
        ns = torch.tensor(next_states[j]).float()
        # target = ((Q(st) - (discount_factor*Q(ns) + re))**2)
        target = re + discount_factor*Q(ns)
        target.backward()
        optimizer.step()

env = RobotHoop(-2,.5,.5, True)
while True:
    a = int(torch.argmax(Q(torch.tensor(env.state()).float())))
    result = env.step(*allactions[a])
    # print(result)
    if result['end']:
        if result['reward'] == 100:
            print('success')
        else:
            print('failure')
        break
    env.vis()
    time.sleep(.1)
