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
      genre1_df = music_data.query(('genre == "{}"').format(genres[genre1]))[feature]
      genre2_df = music_data.query(('genre == "{}"').format(genres[genre2]))[feature]
      
      print("T test for " + feature + ", comparing " + genres[genre1] + " and " + genres[genre2])

      print("Average " + feature + " for " + genres[genre1] + " is " + str(genre1_df.mean()))
      print("Average " + feature + " for " + genres[genre2] + " is " + str(genre2_df.mean()))

      (stat, pvalue) = ttest_ind(genre1_df, genre2_df)
      print("P value is " + str(pvalue) + " so we can" + ("" if pvalue < 0.05 else " NOT") + " assume that there is a statistically significant difference in these genres for this feature\n")

# bar charts of each audio feature
'''plt.figure()
music_data.groupby('genre').agg(np.median).plot(kind = 'barh', subplots=True, sharex=False, legend=None, figsize=(12, 6))
plt.subplots_adjust(wspace=0.5, hspace=0.75);
plt.show(block=True)
'''