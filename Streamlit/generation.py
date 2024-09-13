import pandas as pd 
import streamlit as st 


st.title("Data Generation")

dataset=st.sidebar.radio("Choose the generated dataset you want to display",
                ["Informational Ads - Demographic Groups","Informational Ads - Cognitive Biases",
                 "Commercial Ads - Demographic Groups","Commercial Ads - Cognitive Biases"]
                 )



inf_dg=pd.read_csv("../Data/ads_dg.csv",index_col=0)
inf_cb=pd.read_csv("../Data/ads_cb.csv")

if dataset == "Informational Ads - Demographic Groups" :
    st.markdown("## Informational Ads")
    st.markdown("### Demographic Groups")
    st.dataframe(inf_dg,hide_index=True)
elif dataset == "Informational Ads - Cognitive Biases" :
    st.markdown("## Informational Ads")
    st.markdown("### Cognitive Biases")
    st.dataframe(inf_cb,hide_index=True)
elif dataset == "Commercial Ads - Demographic Groups" : 
    st.markdown("## Commercial Ads")
    st.markdown("### Demographic Groups")
elif dataset == "Commercial Ads - Cognitive Biases" :
    st.markdown("## Commercial Ads")
    st.markdown("### Cognitive Biases")
else : 
    st.write('Please choose a dataset')

