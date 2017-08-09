import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pandas
music_data = pd.read_csv('data.csv')

# visualize
plt.figure()
(music_data['tempo']).plot.hist(alpha=0.5)
plt.show(block=True)