import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('CEMEX interview ppt\GunDeaths_.csv')

print(data.head())

#Drop url column
df = data.drop(columns=['url'])
print(df.head())

#Review unique values of each column
columns = np.array(df.columns)

for i in columns:
    print(i)
    print(df[i].unique())
    print(" ")

# Inconsistent data (integers)
print(df.describe())

print(df.isnull().sum())

#VictimsID duplications
print(df['victimID'].value_counts(ascending=False))

#Add year, month, day and weekday columns
print(df['date'].dtype)
df['date'] = pd.to_datetime(df['date'])
print(df['date'].dtype)

df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month
df['Day'] = df['date'].dt.day
df['Weekday'] = df['date'].dt.weekday

#Count days in months
checker = df.groupby(['Year','Month'])['date'].nunique()
print(checker)

#Weekdayname
weekdays = {0: 'Monday', 1: 'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
df['Weekday_name'] = df['Weekday'].map(weekdays)

#Add Is_holiday column
holidays={datetime.datetime(2012, 12, 25):'Yes',datetime.datetime(2013, 1, 1):'Yes', datetime.datetime(2013, 1, 21):'Yes', datetime.datetime(2013, 2, 18):'Yes', datetime.datetime(2013, 5, 27):'Yes', datetime.datetime(2013, 7, 4):'Yes', datetime.datetime(2013, 10, 14):'Yes', datetime.datetime(2013, 11, 11):'Yes', datetime.datetime(2013, 11, 28):'Yes', datetime.datetime(2013, 12, 25):'Yes'}
df['Is_holiday'] = df['date'].map(holidays)

print(df[df['Is_holiday']=='Yes'])

#Add Identified column
name_cond = df['name'].isnull()
df['Identified'] = np.where(name_cond, 0, 1)
print(df[name_cond])

#Add Demographics column
age_cond = df['age'].isnull()
gender_cond = df['gender'].isnull() 
df['Demographics'] = np.where(age_cond | gender_cond, 0, 1)
print(df[age_cond | gender_cond])

# Define the bins
max_age = df['age'].max()
min_age = df['age'].min()
age_bins = np.round(np.linspace(min_age, max_age, 11).astype(int))
print(age_bins)

# Create the age group variable
age_groups = pd.cut(df['age'], bins=age_bins, include_lowest=True, right=False)
age_groups = age_groups.cat.add_categories('NA')
df['age_group'] = age_groups.fillna('NA')

print(df.groupby('age_group')['victimID'].agg('count'))

#Histrogram for Age dist
sns.histplot(df['age'].dropna(), kde=True)
plt.title('Age distribution')
plt.show()

#Age count
deaths_age = df['age'].value_counts(ascending=False).reset_index().rename(columns={'index':'age', 'age':'deaths'}).sort_values(by='deaths', ascending=False).head(20)
sns.barplot(data=deaths_age, x='age', y='deaths', order = deaths_age['age'])
plt.title('Age distribution')
plt.show()

#Gender distribution
sns.countplot(x='gender', data=df.dropna())
plt.title('Gender distribution')
plt.show()

#Deaths by state
plt.figure(figsize=(10,9))
state_deaths = df.groupby('state')['victimID'].agg('count').sort_values(ascending=False).rename('death_count').reset_index()
print(state_deaths)
sns.barplot(y='state', x='death_count',data=state_deaths)
plt.title('Deaths by State')
plt.show()

#Deaths by state by city
state_city_deaths = df.groupby(['city','state'])['victimID'].agg('count').sort_values(ascending=False).rename('death_count').reset_index().head(10)
print(state_city_deaths)

#Victim Identified
sns.countplot(x='Identified', data=df)
plt.title('Victim identified')
plt.xlabel('Victim identified (1- Yes, 0 - No)')
plt.show()

#Deaths by month
deaths_months = df['Month'].value_counts(ascending=False).reset_index().rename(columns={'index':'month', 'Month':'deaths'}).sort_values(by='deaths', ascending=False)
sns.barplot(data=deaths_months, y='deaths', x='month', order= deaths_months['month'])
plt.title('Deaths by Month')
plt.show()

#Deaths by weekday
deaths_weekday = df['Weekday'].value_counts(ascending=False).reset_index().rename(columns={'index':'weekday', 'Weekday':'deaths'}).sort_values(by='deaths', ascending=False)
sns.barplot(data=deaths_weekday, y='deaths', x='weekday', order= deaths_weekday['weekday'])
plt.title('Deaths by Weekday')
plt.xlabel('Weekday (0 - Monday and so on...)')
plt.show()

#Deaths by weekday
plt.figure(figsize=(10,8))
deaths_day = df['Day'].value_counts(ascending=False).reset_index().rename(columns={'index':'day', 'Day':'deaths'}).sort_values(by='deaths', ascending=False)
sns.barplot(data=deaths_day, y='deaths', x='day', order= deaths_day['day'])
plt.title('Deaths by Day')
plt.xlabel('Day')
plt.show()

#Victim Identified
sns.countplot(x='Identified', data=df)
plt.title('Victim identified (1- Yes, 0 - No)')
plt.show()

#Age distribution by Gender
sns.boxplot(x='gender', y='age', data=df.dropna())
plt.title('Age Distribution by Gender')
plt.show()

#Export document
print(df.head())
df.to_csv('CEMEX interview ppt\gundeaths_modified.csv', index=False)
