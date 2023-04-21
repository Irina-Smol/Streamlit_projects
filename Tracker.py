import streamlit as st
import plotly.graph_objects as go

import calendar
from datetime import datetime 
from streamlit_option_menu import option_menu

# -------------- SETTINGS --------------
incomes = ['Salary', 'Blog', 'Other income']
expenses = ['Rent', 'Car', 'Utilities', 'Saving', 'Other expenses']
currency = 'USD'
page_title = 'Income amd expense tracker'
page_icon = ':money_with_wings:'
layout = 'centered'

# --------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + ' ' + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# --- HIDE STREAMLIT STYLE --- 
hide_st_style = """             
            <style>             
            #MainMenu {visibility: hidden;}             
            footer {visibility: hidden;}            
            header {visibility: hidden;}             
            </style>             
            """ 
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU --- 
selected = option_menu(    
     menu_title=None,     
     options=["Data Entry", "Data Visualization"],     
     icons=["pencil-fill", "bar-chart-fill"],  
     orientation="horizontal", 
)

# --- DATABASE INTERFACE ---
if selected == "Data Entry":
    st.header(f'Data entry is {currency}')
    with st.form('entry_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox('Select month:', months, key='months')
        col2.selectbox('Select year:', years, key='years')

        '---'
        with st.expander('Income'):
            for income in incomes:
                st.number_input(f'{income}: ', min_value=0, format='%i', step=10, key=income)
        with st.expander('Expencses'):
            for expense in expenses:
                st.number_input(f'{expense}: ', min_value=0, format='%i', step=10, key=expense)
        with st.expander('Comment'):
            comment = st.text_area('', placeholder='Enter your comment here...')
        '---'

        submitted = st.form_submit_button('Save data')
        if submitted:
            period = str(st.session_state['years']) + '_' + str(st.session_state['months'])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            st.write(f'incomes: {incomes}')
            st.write(f'expenses: {expenses}')
            st.success("Data saved!")

if selected == "Data Visualization":
    st.header('Data vizualization')
    with st.form('saved_periods'):
        period = st.selectbox('Select period:', ['2023_March'])
        submitted = st.form_submit_button('Plot period')
        if submitted:
            comment = 'Some comment'
            incomes = {'Salary': 1500, 'Blog': 50, 'Other incomes': 500}
            expenses = {'Rent': 600, 'Car': 500, 'Utilities': 200, 'Saving': 300, 'Other expenses': 350}


            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric('Total income', f'{total_income} {currency}')
            col2.metric('Total expense', f'{total_expense} {currency}')
            col3.metric('Remaining budget', f'{remaining_budget} {currency}')
            st.text(f'Comment: {comment}')


            # Create sankey chart  
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())  
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)  
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]  
            value = list(incomes.values()) + list(expenses.values())  
            
            # Data to dict, dict to sankey  
            link = dict(source=source, target=target, value=value)  
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")  
            data = go.Sankey(link=link, node=node)  
            # Plot 
            fig = go.Figure(data)  
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))  
            st.plotly_chart(fig, use_container_width=True)
            fig.show()
