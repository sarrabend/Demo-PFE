import pandas as pd 
import streamlit as st 

st.sidebar.markdown("### Dataset Type")
dataset=st.sidebar.radio("Chsoose the source dataset you want to display",
                 ["Environmental News","Product Descriptions"]
                 )
if dataset=="Environmental News": 
    df=pd.read_csv("../Data/news.csv", index_col=0)
    st.markdown("## The Guardian Environmental News Dataset")
    st.dataframe(df,hide_index=True)
elif dataset == "Product Descriptions":
    df=pd.read_csv("../Data/products.csv", index_col=0)
    st.markdown("## Amazon Products Dataset")
    st.dataframe(df,hide_index=True)
else : 
    st.error("Please select a dataset")