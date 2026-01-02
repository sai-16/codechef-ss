
import pandas as pd
import re

def generate_report(data, feedback, batch, hasfb):
    data = data[data['Batch'] == batch]
    data['Score'] = (
    ((data['Div'] == 3.0) & (data['Solved Count'] >= 1)).astype(int)
    +
    ((data['Div'] == 4.0) & (data['Solved Count'] >= 2)).astype(int)
    +
    ((data['Div'] ==4.0) & (data['Solved Count'] >= 4)).astype(int)
    +
    ((data['Div'] ==3.0) & (data['Solved Count'] >= 2)).astype(int) 
    +
    ((data['Div'] ==2.0) & (data['Solved Count'] >= 1)).astype(int)
    +
    ((data['Div'] ==2.0) & (data['Solved Count'] >= 1)).astype(int) 
        
    )

    data['Score'] = (data['Score']).astype(int)
    no = num = int(re.search(r'\d+', data['Selected Contest'].iloc[0]).group())
    print(no)
    data['Participated'] = data['Status']=="YES"
    # print(data['Participated'].value_counts())
    print(feedback.columns[-1])
    feedback.rename(columns={feedback.columns[-2]: 'Roll Number'}, inplace=True)
    feedback.rename(columns = {feedback.columns[-1]: 'Feedback'},inplace=True)
    data['Roll Number'] = data['Roll Number'].str.lower()
    feedback['Roll Number'] = feedback['Roll Number'].str.lower()
    data = pd.merge(data, feedback, on='Roll Number', how='left')
    # print(data['Feedback'].value_counts())
    data['Solved Count'] = data['Solved Count'].fillna(0).astype(int)
    if hasfb:
        data['Feedback'] = data.apply(
            lambda row: (
                f"CODECHEF-START{no} ATTENDED DIV : {int(row['Div'])} , SOLVED : {row['Solved Count']} - ({row['Codechef']})"
                if row['Participated'] 
                else (
                    f"CODECHEF-START{no} DID NOT PARTICIPATE, REASON - {row['Feedback']} - ({row['Codechef']})"
                    if pd.notna(row['Feedback']) and row['Feedback'].strip() != ""
                    else f"CODECHEF-START{no} DID NOT PARTICIPATE - ({row['Codechef']})"
                )
            ),
            axis=1
        )
    else:
        data['Feedback'] = data.apply(
            lambda row: (
                f"CODECHEF-START{no} ATTENDED DIV : {int(row['Div'])}, SOLVED : {row['Solved Count']} - ({row['Codechef']})"
                if row['Participated']
                else f"CODECHEF-START{no} DID NOT PARTICIPATE - ({row['Codechef']})"
            ),
            axis=1
        )
    print(data.head())
    df = data[['Email', 'Roll Number', 'Score','Feedback']]
    df.set_index("Email", inplace=True)
    # df.rename(columns={'Email': 'email'}, inplace=True)
    df.rename(columns={'Roll Number': 'RollNumber'}, inplace=True)
    df['RollNumber'] = df['RollNumber'].str.upper()
    return df
    
