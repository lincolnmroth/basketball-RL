import numpy as np
import math
import matplotlib.pyplot as plt

class RobotHoop:

    def __init__(self, hoop_x, hoop_y, hoop_rad, vis):
        self.l1 = 1;
        self.l2 = 1;
        self.hoop_x = hoop_x
        self.hoop_y = hoop_y
        self.hoop_rad = hoop_rad
        self.theta1=0;
        self.theta2=0;
        self.x=0;
        self.y=0;
        self.xdot=0;
        self.ydot=0;
        self.theta1dot=0;
        self.theta2dot=0;
        if vis:
            fig = plt.figure()
            self.ax = plt.axes()
            plt.ion()


    def closeFig(self):
        plt.close()

    def shootHoop(self):
        self.updateXY()
        # print(self.x, self.y, self.xdot, self.ydot)

        if self.ydot <= 0:
            return -1
        try:
            t1 = (-1*self.ydot + math.sqrt(self.ydot**2 - (4*-5*(self.y -self.hoop_y))))/(-5)
            t2 = (-1*self.ydot - math.sqrt(self.ydot**2 - (4*-5*(self.y -self.hoop_y))))/(-5)
            return (self.x + self.xdot*t1,self.x + self.xdot*t2)
        except:
            return -1

        if (self.x + self.xdot*t1 < self.hoop_x+self.hoop_rad and  self.x + self.xdot*t1 > self.hoop_x-self.hoop_rad) or (self.x + self.xdot*t2 < self.hoop_x+self.hoop_rad and  self.x + self.xdot*t2 > self.hoop_x-self.hoop_rad):
            return True

    def updateXY(self):
        self.x = self.l1*math.cos(self.theta1) + self.l2*math.cos(self.theta1+self.theta2)
        self.y = self.l1*math.sin(self.theta1) + self.l2*math.sin(self.theta1+self.theta2)
        self.xdot = self.l1*math.cos(self.theta1dot) + self.l2*math.cos(self.theta1dot+self.theta2dot);
        self.ydot = self.l1*math.sin(self.theta1dot) + self.l2*math.sin(self.theta1dot+self.theta2dot);

    def vis(self):

        self.updateXY()
        a = self.l1*math.cos(self.theta1)
        b = self.l1*math.sin(self.theta1)
        plt.cla()
        self.ax.set_xlim(-2, 5)
        self.ax.set_ylim(-3,3)
        self.ax.plot([0, a], [0, b])
        self.ax.plot([a, self.x], [b, self.y])
        self.ax.plot([self.hoop_x-(self.hoop_rad), self.hoop_x+(self.hoop_rad)], [self.hoop_y, self.hoop_y])
        plt.draw()
        plt.pause(0.001)

    def state(self):
        return np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0])

    def step(self, action1, action2, release):
        # self.vis()
        if not release:
            if action1 == 'f':
                self.theta1dot = min(self.theta1dot+.1, 2)
            if action1 == 's':
                self.theta1dot = max(self.theta1dot-.1, -2)
            if action2 == 'f':
                self.theta2dot = min(self.theta2dot+.1, 2)
            if action2 == 's':
                self.theta2dot = max(self.theta2dot-.1, -2)

            self.theta1 += self.theta1dot
            # self.theta1 = max(min(self.theta1, .5), -.5)
            self.theta2 += self.theta2dot
            # self.theta2 = max(min(self.theta2, .5), -.5)

            if self.theta1 > 1 or self.theta1 < -1 or self.theta2 > 1 or self.theta2 < -1:
                return {'reward':-300, 'state':np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0]), 'end':True}


            return {'reward':-1, 'state':np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0]), 'end':False}

        else:
            # print('throwing')
            xvalues = self.shootHoop()
            if xvalues == -1:
                return {'reward':-100, 'state':np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0]), 'end':True}
            elif (xvalues[0] < self.hoop_x+self.hoop_rad and  xvalues[0] > self.hoop_x-self.hoop_rad) or (xvalues[1] < self.hoop_x+self.hoop_rad and  xvalues[1] > self.hoop_x-self.hoop_rad):
                return {'reward':100, 'state':np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0]), 'end':True}
            else:
                return {'reward':-100, 'state':np.array([self.theta1dot, self.theta2dot, self.theta1, self.theta2, 0]), 'end':True}
