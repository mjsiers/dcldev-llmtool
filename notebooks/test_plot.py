#%%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#%%
clients_reasons_filename = "../data/client_reasons_info.csv"
df_reasons = pd.read_csv(clients_reasons_filename)
df_reasons = df_reasons[df_reasons['percent'] > 0.5]
print(df_reasons.shape)
print(df_reasons.head())


#%%
plt.figure(figsize=(10, 6))
sns.barplot(data=df_reasons, x='percent', y='keyword')
plt.title('Assessment Key Reasons')
plt.xlabel('Percentage')
plt.ylabel('Parent Keyword')
plt.savefig('parent-keywords.png')
plt.show()


#%%
clients_info_filename = "../data/client_info.csv"
df_clients = pd.read_csv(clients_info_filename)
df_clients.drop(columns=["assessment_uuid", "assessment_reasons", "assessment_keywords"], inplace=True)
df_clients["assessment_year"] = df_clients["assessment_date"].str[0:4]
print(df_clients.shape)
print(df_clients.head())


#%%
list_years = ["2021", "2022", "2023", "2024"]
df_clients = df_clients[df_clients["assessment_year"].isin(list_years)]
print(df_clients.shape)

df_clients = df_clients[df_clients["client_age"] < 25]
print(df_clients.shape)


#%%
plt.figure(figsize=(10, 6))
sns.histplot(data=df_clients, x='client_age', hue='assessment_year', stat="percent", multiple="stack")
plt.title('Client Ages [2021-2024]')
plt.ylabel('Percentage')
plt.savefig('client-ages.png')
plt.show()


#%%
plt.figure(figsize=(10, 6))
sns.histplot(data=df_clients, x='client_grade', hue='assessment_year', stat="percent", multiple="stack", discrete=True)
plt.title('Client Grades [2021-2024]')
plt.ylabel('Percentage')
plt.savefig('client-grades.png')
plt.show()


#%%
