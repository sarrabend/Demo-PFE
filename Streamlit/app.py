import streamlit as st 

data_page = st.Page("data.py", title="Data Overview")
demo_page = st.Page("demo.py", title="Example Demo")
generation_page = st.Page("generation.py", title="Generation")
evaluation_page = st.Page("evaluation.py", title="Evaluation")
pg = st.navigation([data_page, demo_page, generation_page, evaluation_page])

pg.run()