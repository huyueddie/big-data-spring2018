import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline
rng = pd.date_range('1/1/2011', periods=72, freq='H')
rng
pd.Period('2011-01')
print(pd.Period('2011-01'))
dates = [pd.Timestamp('2012-05-01'), pd.Timestamp('2012-05-02'), pd.Timestamp('2012-05-03')]
print(dates)
ts = pd.Series(np.random.randn(3), dates)
print(ts)
periods = [pd.Period('2012-01'), pd.Period('2012-02'), pd.Period('2012-03')]
print(periods)
