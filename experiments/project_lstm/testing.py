import streamlit as st, pandas as pd, numpy as np

st.title('Streamlit for Financial Programming')
st.header('Streamlit header')
st.subheader('Streamlit Sub header')
st.write('My content will be written here!')
st.caption('My captions are here!')

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]})

st.write(df)
x = st.sidebar.slider('x',0,10)
st.write(x*x)

if st.sidebar.checkbox('Checkbox'):
    st.balloons()

y = st.sidebar.text_input('Name')
st.write(y)

st.number_input('Number',50,100)
st.date_input('Date Input')
option = st.selectbox('Which number do you like best?',[1, 2, 3, 4])
st.write('You selected: ', option)

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

left, right = st.columns(2)

left.write('I am the left Side!')
with right:
    st.write('I am the Right Side!')

tab1, tab2, tab3 = st.tabs(['Streamlit1','Streamlit2','Streamlit3'])

with tab1:
   st.header("first tab")
   
with tab2:
   st.header("Second tab")
   
with tab3:
   st.header("Thrid tab")


import time
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)