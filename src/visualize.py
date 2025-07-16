import pandas as pd
from main import main
import streamlit as st

st.set_page_config(layout='wide')

if 'raw' not in st.session_state:
    st.session_state.raw = main('https://obasen.orientering.se/winsplits/online/en/default.asp?page=table&databaseId=106439&categoryId=2',
         [],False,[],5,'else')
raw = st.session_state.raw['results']

with st.sidebar:
    personal_position = st.slider('your position',1,len(raw))
    personal_name = raw[personal_position-1]['name']
    st.markdown(f'you are {personal_name}!')
    interest = [personal_position]
    interest.append(1)

df = pd.DataFrame()

for item in interest:
    results = pd.DataFrame(raw[item-1]['splits'])
    if item == personal_position:
        df['gap'] = results['split_gap']
        df['perc'] = results['percentage_gap']
    df[raw[item-1]['name']] = results['time']
df = df.drop(index=len(df)-1)
for i in df.index:
    df.at[i,'control'] = i+1

st.subheader(f'Split gaps for the athlete **{personal_name}**')
left,right = st.columns([0.15, 0.85])
show = left.radio('show',['absolute gap','relative gap'])
y = 'gap' if show == 'absolute gap' else 'perc'
y_label = 's' if show == 'absolute gap' else '%'
right.bar_chart(df,x='control',y=y, y_label=y_label)