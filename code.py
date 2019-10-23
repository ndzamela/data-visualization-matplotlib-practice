# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
data_ipl = pd.read_csv(path)
data_ipl['year'] = data_ipl['date'].apply(lambda x : x[:4])

# Plot the wins gained by teams across all seasons
matches_won = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)
print(matches_won)
# count the number of unique occurrences within a column by value(team)
total_wins = matches_won['winner'].value_counts()
print(total_wins)
plot_wins = total_wins.plot(kind='bar', title="Total number of wins by team across all seasons", figsize=(7,5))
plt.xticks(fontsize=10, rotation=45)
# Plot Number of matches played by each team through all seasons
temp_data = pd.melt(matches_won, id_vars=['match_code','year'], value_vars=['team1','team2'])
#print(temp_data)
matches_played = temp_data.value.value_counts()
#matches_played

plt.figure(figsize=(12,6))
matches_played.plot(x=matches_played.index, y=matches_played, kind='bar',title='No of matches played across 9 seaons')
plt.xticks(rotation='vertical')
plt.show()



# Top bowlers through all seasons



# Top bowlers through all seasons
#print(data_ipl['wicket_kind'].value_counts())

wickets = data_ipl[(data_ipl['wicket_kind']=='bowled') | (data_ipl['wicket_kind'] == 'caught') | (data_ipl['wicket_kind']=='lbw') | (data_ipl['wicket_kind']=='caught and bowled') ]
print(wickets)

bowlers_wickets = wickets.groupby(['bowler'])['wicket_kind'].count()
#print(bowlers_wickets)

bowlers_wickets.sort_values(ascending=False, inplace=True)

#bowlers_wickets[:10].plot(x = bowlers_wickets.index, y=bowlers_wickets, kind='barh', colormap='gist_rainbow')

score_per_stadium = data_ipl.loc[:, ['match_code','venue','inning','total']]
#print(score_per_stadium)
average_score_per_stadium = score_per_stadium.groupby(['match_code','venue','inning']).agg({'total':'sum'}).reset_index()
#print(average_score_per_stadium)
average_score_per_stadium = average_score_per_stadium.groupby(['venue','inning'])['total'].mean().reset_index()

#print("-----------Group by on venue and inning and apply mean function-----------")
#print(average_score_per_stadium)

average_score_per_stadium = average_score_per_stadium[(average_score_per_stadium['inning']==1) | (average_score_per_stadium['inning']==2)]
# How did the different pitches behave? What was the average score for each stadium?
plt.figure(figsize=(19,8))
plt.plot(average_score_per_stadium[average_score_per_stadium['inning']==1]['venue'],average_score_per_stadium[average_score_per_stadium['inning']==1]['total'],'-y',marker='v',ms=15,lw=10,label='inning1')
plt.plot(average_score_per_stadium[average_score_per_stadium['inning']==2]['venue'],average_score_per_stadium[average_score_per_stadium['inning']==2]['total'],'-r',marker='v',ms=15,lw=10,label='inning2')
plt.legend(loc='upper right', fontsize=19)
plt.xticks(fontsize=15, rotation=90)
plt.xlabel('Venues', fontsize=18)
plt.ylabel('Average runs scored by venues', fontsize=16)
plt.show()


# How did the different pitches behave? What was the average score for each stadium?
plt.figure(figsize=(19,8))
plt.plot(average_score_per_stadium[average_score_per_stadium['inning']==1]['venue'],average_score_per_stadium[average_score_per_stadium['inning']==1]['total'],'-y',marker='v',ms=15,lw=10,label='inning1')
plt.plot(average_score_per_stadium[average_score_per_stadium['inning']==2]['venue'],average_score_per_stadium[average_score_per_stadium['inning']==2]['total'],'-r',marker='v',ms=15,lw=10,label='inning2')
plt.legend(loc='upper right', fontsize=19)
plt.xticks(fontsize=15, rotation=90)
plt.xlabel('Venues', fontsize=18)
plt.ylabel('Average runs scored by venues', fontsize=16)
plt.show()

# Types of Dismissal and how often they occur
dismissed = data_ipl.groupby(['wicket_kind']).count().reset_index()
dismissed = dismissed[['wicket_kind','delivery']]
dismissed = dismissed.rename(columns={'delivery':'count'})



print("dimissed with wicked kind series")
print(dismissed["wicket_kind"])
f, (ax1, ax2) = plt.subplots(1,2,figsize=(15,7))
f.suptitle("Top 5 Dimissal Kind", fontsize=14)

dismissed.plot.bar(ax=ax1, legend=False)
ax1.set_xticklabels(list(dismissed["wicket_kind"]), fontsize=8)

explode = [0.80,0.01,0.1,0.2,0.25,0.4,0.35,0.05,0.05]
properties = ax2.pie(dismissed["count"], labels=None, startangle=150, autopct='%1.1f%%',explode = explode)
ax2.legend(bbox_to_anchor=(1,1), labels=dismissed['wicket_kind'])

# Plot no. of boundaries across IPL seasons
boundaries_data = data_ipl.loc[:, ['runs' ,'year']]
boundaries_fours = boundaries_data[boundaries_data['runs']==4]
fours = boundaries_fours.groupby('year')['runs'].count()
boundaries_six = boundaries_data[boundaries_data['runs']==6]
six = boundaries_six.groupby('year')['runs'].count()

plt.figure(figsize=(12,8))
plt.plot(fours.index, fours, '-b', marker='o', ms=6, lw=2, label='fours')
plt.plot(six.index, six,'-r', marker='o', ms=6,lw=2, label='sixes')
plt.legend(loc= 'upper right', fontsize=19)
plt.xticks(fontsize=15, rotation=90)
plt.xlabel('IPL Seasons', fontsize=18)
plt.ylabel('Total 4s and 6s scored across seasons', fontsize=16)
plt.show()

# Average statistics across all seasons
per_match_data = data_ipl.drop_duplicates(subset='match_code',keep='first').reset_index(drop=True)
total_runs_per_season = data_ipl.groupby('year')['total'].sum()
total_deliveries_per_season = data_ipl.groupby('year')['delivery'].count()
no_of_matches_per_season = per_match_data.groupby('year')['match_code'].count()

print("------Total Runs per Season-----------")
print(total_runs_per_season)
print("------Total Deliveries per Season-----------")
print(total_deliveries_per_season)
print("------No of matches per season-----------")

print(no_of_matches_per_season)

avg_runs_per_match = total_runs_per_season / no_of_matches_per_season
avg_balls_per_match = total_deliveries_per_season / no_of_matches_per_season
avg_runs_per_ball = total_runs_per_season /  total_deliveries_per_season

avg_data = pd.DataFrame([no_of_matches_per_season, avg_runs_per_match,avg_balls_per_match, avg_runs_per_ball ])
avg_data.index = ['No of Matches', 'Average Runs per Match', 'Average Balls Bowled per Match', 'Average Runs per Ball']

print(avg_data)

print("Transpose a DataFrame")
print(avg_data.T)

avg_data.T.plot(kind='bar',figsize=(12,10), colormap='coolwarm')
plt.xlabel('Season')
plt.ylabel('Average')
plt.legend(loc=9,ncol=4)




