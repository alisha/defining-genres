import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# pandas
music_data = pd.read_csv('data.csv')

# bar charts of each audio feature
plt.figure()
music_data.groupby('genre').agg(np.median).plot(kind = 'barh', subplots=True, sharex=False, legend=None, figsize=(12, 6))
plt.subplots_adjust(wspace=0.5, hspace=0.75);
plt.show(block=True)
