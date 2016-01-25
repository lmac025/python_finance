""" # The Black Scholes Formula
# CallPutFlag - This is set to 'c' for call option, anything else for put
# S - Stock price
# K - Strike price
# T - Time to maturity
# r - Riskfree interest rate
# d - Dividend yield
# v - Volatility
"""
from scipy.stats import norm
from math import *
def BlackScholes(CallPutFlag,S,K,T,r,d,v):
	d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*sqrt(T))
	d2 = d1-v*sqrt(T)
	if CallPutFlag=='c':
		return S*exp(-d*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
	else:
		return K*exp(-r*T)*norm.cdf(-d2)-S*exp(-d*T)*norm.cdf(-d1)

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

plt.clf()
fig,ax = plt.subplots()
maturity = 0
S = np.linspace(80,120,200)
p = []
for i in S:
	p.append(BlackScholes('c', i, 100, 0.005, 0.06, 0, 0.4))

line, = ax.plot(p)
#ax.set_ylim()

def update(step):
	p = []
	for i in S:
		p.append(BlackScholes('c', i, 100, step, 0.06, 0, 0.4))
	line.set_ydata(p)
	
def data_gen():
	expStop = 0.0005
	expStart = 1.5
	T = np.linspace(expStop,expStart,200)
	m = -log(expStop/expStart)/expStart
	for t in T:
		yield expStart*exp(-m*t)

ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()