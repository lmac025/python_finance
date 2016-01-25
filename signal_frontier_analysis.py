import matplotlib.pyplot as plt
from collections import defaultdict

#stock tickers
names = ['AAPL', 'GOOG', 'MSFT', 'DELL', 'GS', 'MS', 'BAC', 'C']

def heatmap(df, cmap=plt.cm.gray_r):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
	ax.set_xlabel(df.columns.name)
	ax.set_xticks(np.arange(len(df.columns)))
	ax.set_xticklabels(list(df.columns))
	ax.set_ylabel(df.index.name)
	ax.set_yticks(np.arange(len(df.index)))
	ax.set_yticklabels(list(df.index))
	plt.colorbar(axim)

def get_px(stock, start, end):
	return web.get_data_yahoo(stock, start, end)['Adj Close']
	
def calc_mom(price, lookback, lag):
	mom_ret = price.shift(lag).pct_change(lookback)
	ranks = mom_ret.rank(axis=1, ascending=False)
	demeaned = ranks - ranks.mean(axis=1)
	return demeaned / demeaned.std(axis=1)

def strat_sr(prices, lb, hold):
	# Compute portfolio weights
	freq = '%dB' % hold
	port = calc_mom(prices, lb, lag=1)
	daily_rets = prices.pct_change()
	# Compute portfolio returns
	port = port.shift(1).resample(freq, how='first')
	returns = daily_rets.resample(freq, how=compound)
	port_rets = (port * returns).sum(axis=1)
	return daily_sr(port_rets) * np.sqrt(252 / hold)	
	
px = DataFrame({n: get_px(n, '1/1/2009', '6/1/2012') for n in names})

px = px.asfreq('B').fillna(method='pad')
rets = px.pct_change()
((1 + rets).cumprod() - 1).plot()

compound = lambda x : (1 + x).prod() - 1
daily_sr = lambda x: x.mean() / x.std()

strat_sr(px, 70, 30)

lookbacks = range(20, 90, 5)
holdings = range(20, 90, 5)
dd = defaultdict(dict)
for lb in lookbacks:
	for hold in holdings:
		sdd[lb][hold] = strat_sr(px, lb, hold)

ddf = DataFrame(dd)
ddf.index.name = 'Holding Period'
ddf.columns.name = 'Lookback Period'

heatmap(ddf)	
	
