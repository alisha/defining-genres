import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import ttest_ind

# pandas
music_data = pd.read_csv('data.csv', sep='|', error_bad_lines=False)

genres = ['indie', 'pop', 'rap', 'country']
features = ['danceability', 'energy', 'speechiness', 'tempo']

# t test
for feature in features:
  for genre1 in range(0, len(genres)):
    for genre2 in range(genre1 + 1, len(genres)):
      print("T test for " + feature + ", comparing " + genres[genre1] + " and " + genres[genre2])
      (stat, pvalue) = ttest_ind(music_data.query(('genre == "{}"').format(genres[genre1]))[feature], music_data.query(('genre == "{}"').format(genres[genre2]))[feature])
      print("P value is " + str(pvalue) + " so we can" + ("" if pvalue < 0.05 else " NOT") + " assume that there is a statistically significant difference in these genres for this feature\n")

# bar charts of each audio feature
'''plt.figure()
music_data.groupby('genre').agg(np.median).plot(kind = 'barh', subplots=True, sharex=False, legend=None, figsize=(12, 6))
plt.subplots_adjust(wspace=0.5, hspace=0.75);
plt.show(block=True)
'''