# %%
import math
import numpy as np
import pandas as pan
import matplotlib.pyplot as plt

# %% [markdown]
# ### **Executing Karger Stein**

# %%
df = pan.read_csv('output_kargerstein.csv',header=None)
print(df)

# %%
df_karger=df
df_karger.columns = ['dataset','n_vertices', 'n_edges', 'time', 'time_in_s', 'result','discovery_time','rep','k','k_min'] # Add Column Headings

df_karger.drop(['dataset'], inplace=True, axis=1) # Remove the custom Index
#print(df_karger)
print(df_karger)

# %%
current_n_vertices = 0
sum_times = 0.0
sum_edges = 0

df_karger_new = pan.DataFrame()

for index, row in df_karger.iterrows():

  if current_n_vertices == 0:
    current_n_vertices = row['n_vertices']
  
  if current_n_vertices != row['n_vertices']:
    df_karger_temp= pan.DataFrame({'n_vertices': int(current_n_vertices), 'mean_edges': (sum_edges / 4), 'time': (sum_times / 4)}, index=[0])
    df_karger_new = pan.concat([df_karger_new, df_karger_temp], ignore_index=True)

    current_n_vertices = row['n_vertices']
    sum_times = 0.0
    sum_edges = 0

  if index == (df.shape[0]):
    sum_times += float(row['time'])
    sum_edges += int(row['n_edges'])
    df_karger_temp = pan.DataFrame({'n_vertices': int(current_n_vertices), 'mean_edges': (sum_edges / 4), 'time': (sum_times / 4)}, index=[0])
    df_karger_new = pan.concat([df_karger_new, df_karger_temp], ignore_index=True)
  else:
    sum_times += float(row['time'])
    sum_edges += int(row['n_edges'])

print(df_karger_new)

# %%
ratios = [None] + [round(df_karger_new.iloc[i + 1]['time'] / df_karger_new.iloc[i]['time'], 6) for i in range((df_karger_new.shape[0] - 1))]
ratios

# %%
c_estimates = [round(df_karger_new.iloc[i]['time'] / (float(df_karger_new.iloc[i]['mean_edges']) * float(df_karger_new.iloc[i]['n_vertices'])), 6) for i in range(df_karger_new.shape[0])]
c_estimates

# %%
reference = []
for i in range(df_karger_new.shape[0]):
  reference = [round(85.029095 * float(df_karger_new.iloc[i]['mean_edges']) * float(df_karger_new.iloc[i]['n_vertices']), 6) for i in range(df_karger_new.shape[0])]

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)
ax.plot(df_karger_new['n_vertices'], df_karger_new['time'], label='Computational complexity of the algorithm')
ax.plot(df_karger_new['n_vertices'], reference, label='Theoretical(C) computational complexity of the algorithm')
ax.set_title('Kruskal algorithm, Naive Version')
plt.xlabel('Number of nodes')
plt.ylabel('Time (in nanoseconds)')
ax.legend()
plt.savefig('kruskal_naive.png')
plt.show()
