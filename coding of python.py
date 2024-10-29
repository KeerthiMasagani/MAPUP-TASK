import pandas as pd

# Sample data (replace with actual data loading code)
data = pd.DataFrame({
    'player_id': [1, 2, 1, 3, 2],
    'date': ['2023-10-02', '2023-10-02', '2023-10-16', '2023-10-18', '2023-10-26'],
    'slot': ['S1', 'S1', 'S2', 'S1', 'S2'],
    'deposit': [1000, 500, 1200, 300, 700],
    'withdrawal': [500, 300, 400, 200, 500],
    'games_played': [10, 20, 30, 5, 15],
    'deposit_count': [3, 2, 4, 1, 3],
    'withdrawal_count': [1, 1, 2, 0, 1]
})

# Function to calculate loyalty points for each entry
def calculate_loyalty_points(row):
    deposit_points = 0.01 * row['deposit']
    withdrawal_points = 0.005 * row['withdrawal']
    balance_count_points = 0.001 * max(row['deposit_count'] - row['withdrawal_count'], 0)
    games_points = 0.2 * row['games_played']
    return deposit_points + withdrawal_points + balance_count_points + games_points

# Apply function to calculate points
data['loyalty_points'] = data.apply(calculate_loyalty_points, axis=1)

# Calculate daily slot-based points
daily_slot_points = data.groupby(['player_id', 'date', 'slot'])['loyalty_points'].sum().reset_index()

# Calculate overall monthly loyalty points and ranking
monthly_points = data.groupby('player_id').agg({
    'loyalty_points': 'sum',
    'games_played': 'sum'  # For tie breaking
}).sort_values(by=['loyalty_points', 'games_played'], ascending=[False, False]).reset_index()

# Calculate bonus allocation for top 50 players
top_50 = monthly_points.head(50)
total_points = top_50['loyalty_points'].sum()
top_50['bonus'] = (top_50['loyalty_points'] / total_points) * 50000

# Average deposit amount and average games per user
average_deposit = data['deposit'].mean()
average_deposit_per_user = data.groupby('player_id')['deposit'].mean().mean()
average_games_per_user = data.groupby('player_id')['games_played'].mean().mean()

# Results
print("Daily Slot Points:\n", daily_slot_points)
print("Monthly Points and Ranking:\n", monthly_points)
print("Top 50 Players with Bonus:\n", top_50[['player_id', 'loyalty_points', 'bonus']])
print("Average Deposit Amount:", average_deposit)
print("Average Deposit per User:", average_deposit_per_user)
print("Average Games Played per User:", average_games_per_user)
