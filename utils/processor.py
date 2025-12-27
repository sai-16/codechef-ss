
import pandas as pd
import re

def generate_report(data, feedback, batch, hasfb):
    data = data[data['Batch'] == batch].copy()

    data['Score'] = (
        ((data['Div'] == 3.0) & (data['Solved Count'] >= 1)).astype(int) +
        ((data['Div'] == 4.0) & (data['Solved Count'] >= 2)).astype(int) +
        ((data['Div'] == 4.0) & (data['Solved Count'] >= 4)).astype(int) +
        ((data['Div'] == 3.0) & (data['Solved Count'] >= 2)).astype(int) +
        ((data['Div'] == 2.0) & (data['Solved Count'] >= 1)).astype(int)
    )

    no = int(re.search(r'\d+', data['Selected Contest'].iloc[0]).group())
    data['Participated'] = data['Status'] == "YES"

    feedback.rename(columns={
        feedback.columns[-2]: 'Roll Number',
        feedback.columns[-1]: 'Feedback'
    }, inplace=True)

    data['Roll Number'] = data['Roll Number'].str.lower()
    feedback['Roll Number'] = feedback['Roll Number'].str.lower()

    data = pd.merge(data, feedback, on='Roll Number', how='left')

    data['Feedback'] = data.apply(
        lambda r: f"CODECHEF-START{no} ATTENDED - ({r['Codechef']})"
        if r['Participated']
        else f"CODECHEF-START{no} DID NOT PARTICIPATE - ({r['Codechef']})",
        axis=1
    )

    df = data[['Email', 'Roll Number', 'Score', 'Feedback']]
    df.set_index("Email", inplace=True)
    df.rename(columns={'Roll Number': 'RollNumber'}, inplace=True)
    df['RollNumber'] = df['RollNumber'].str.upper()
    return df
