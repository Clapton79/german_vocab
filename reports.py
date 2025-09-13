import pandas as pd

df = pd.read_csv('test_results.csv')

# add a column for date only (without time)
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Summarize results by the new date column, number of questions and accuracy rounded to a whole number
summary = df.groupby(['Date']).agg(
    Number_of_questions=('Number of questions', 'sum'),
    Good_answers=('Accuracy', lambda x: (round(x/100 * df.loc[x.index, 'Number of questions'],0)).sum()),
    Accuracy_pct=('Accuracy', lambda x: round(x.mean(), 2))
    )

print(summary)