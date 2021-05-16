from RobotHoop import RobotHoop
import random, time
import numpy as np
import matplotlib.pyplot as plt

Q = np.zeros((40, 40, 21, 21, 2, 10))

discount_factor = .2
alpha = .6
epsilon = .2
iterations = 100000
maxsteps = 1000
actions = [('f', 'f', False), ('f', 's', False), ('f', '', False), ('s', 'f', False), ('s', 's', False), ('s', '', False), ('', 'f', False), ('', 's', False), ('','',False), ('', '', True)]

rewards = np.zeros(iterations)
scores = np.zeros(iterations)
scoretot = 0
for i in range(iterations):
    dovis=False
    if i%1000 == 999:
        dovis = True
    env = RobotHoop(-2,.5,.5, dovis)
    # alpha = 1/(i+1)
    # epsilon = 1/(math.sqrt(i+1))
    for j in range(maxsteps):
        initial_state = env.state()
        actions_q = Q[int(10*env.state()[0]), int(10*env.state()[1]), int(10*env.state()[2]), int(10*env.state()[3]), int(env.state()[4])]
        best_action = np.argmax(actions_q)
        ran = random.uniform(0,1)
        if ran > epsilon :
            action = best_action
        else:
            action = random.randrange(10)

        old_q = actions_q[action]

        res = env.step(*actions[action])
        rewards[i] += res['reward']
        new_actions_q = Q[int(10*env.state()[0]), int(10*env.state()[1]), int(10*env.state()[2]), int(10*env.state()[3]), int(env.state()[4])]
        best_next = np.argmax(new_actions_q)
        newQ = (1-alpha)*(old_q) + alpha*(res['reward'] + discount_factor*max(new_actions_q))
        Q[int(10*initial_state[0]), int(10*initial_state[1]), int(10*initial_state[2]), int(10*initial_state[3]), int(initial_state[4]), action] = newQ

        if res['end']:
            if res['reward'] == 100:
                print('win')
                scoretot += 1
                scores[i] = scoretot/i
                pass
            else:
                pass
            break

        if dovis:
            env.vis()
            time.sleep(.1)

    if dovis:
        env.closeFig()
print(max(rewards))
plt.plot(scores)

plt.show()
