# Reinforcement Learning Basketball
Robot Arm learning basketball using NFQ and Q-Learning


![basketball](https://user-images.githubusercontent.com/14778866/118385135-6e1fae00-b5da-11eb-9277-74c7b2fef7be.gif)

##Methods
###Q-Learning (Q Table)
Q-learning is slightly rudimentary but it had quite successful results. It uses a table of all possible states and uses the following equuation to explore and discover an optimal policy:

![image](https://user-images.githubusercontent.com/14778866/118385001-1f254900-b5d9-11eb-99ad-3978cb74d18c.png)


###NFQ (Neural Fitted Q-Iteration)
NFQ uses a neural network to learn the Q values.

First a bunch of data is created using a random policy. Then a 2-layer neural net using PyTorch and a RPROP optimizer is created. Training was done target seen in the algorithm below.
![image](https://user-images.githubusercontent.com/14778866/118385043-80e5b300-b5d9-11eb-9021-c87c3cdfd38a.png)


# Conclusions and Future 
There were a lot of issues and there are still are. Firstly and most easily fixed is to change to a dynamic alpha and exploration value (epsilon) in the q-table variant. Much much more work can be done on the nfq side to create a better structured neural net as well tune the other various parameters.
