import pandas as pd
import streamlit as st 
import time 
import numpy as np 
import json 


st.title("Example Demo : running the pipeline on an article from the Guardian News dataset")
#  Generation 
st.markdown("## **Select an Article**")
df3=pd.read_csv("../Data/ads_dg.csv",index_col=0)
title = st.selectbox("Choose Title",df3["Title"])
row=df3.loc[df3['Title'] == title]
id=row.index[0]
st.dataframe(row[["Title",'Intro',"Text"]],hide_index=True)


st.markdown("## **Ad Generation**")
prompt = st.selectbox("Prompt version",("Prompt 1","Prompt 2","Prompt 3"))



if prompt=="Prompt 1" : 
## Template 1 
    st.text_area("Prompt Text","Generate 5 ad variations for the following news article : A neutral Ad, 2 variations targeting different age groups : young adults and elderly people, 2 variations targeting distinct genders : men and women. {article}")
    if st.button("Generate") :
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(1, 101):
            progress_bar.progress(i)
            time.sleep(0.02)
        df1=pd.read_csv("../Data/ads_dg_0.csv")
        row_1=df1.loc[df1['Title'] == title]
        st.dataframe(row_1[["neutral","young_adults","elderly_people","men","women"]],hide_index=True)

if prompt=="Prompt 2" : 
## Template  2
    st.text_area("Prompt Text",'''Generate 5 ad variations for the following news article.
The 5 ads should include :

1. **A neutral Ad:** The first ad should be a neutral advertisement without targeting any group of people.
2. **2 variations targeting different age groups:** Create two variations of the ad, each addressed to a certain age range. Take into account the following age groups: young adults and elderly people.
3. **2 variations targeting distinct genders:** Make two versions of the advertisement, one for each gender men and women.

**Instructions:**

- Craft each ad with a headline and a short body text (without exceeding two lines) that persuades potential customers to engage with its content.

{article}''', height=400)
    # st.button("Generate", type="primary")
    if st.button("Generate") :
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(1, 101):
            progress_bar.progress(i)
            time.sleep(0.03)
        df2=pd.read_csv("../Data/ads_dg_1.csv")
        row_2=df2.loc[df2['Title'] == title]
        st.dataframe(row_2[["neutral","young_adults","elderly_people","men","women"]],hide_index=True)

if prompt=="Prompt 3" : 
## Template 3 
    st.text_area("Prompt Text",'''Generate 5 headlines and concise descriptions of the following article :

The variations should include :

1. **neutral:** The first one should be neutral without targeting any group of people.
2. **2 variations targeting different age groups:** Create two variations, each addressed to a certain age range.
Take into account the following age groups: young adults and elderly people.
3. **2 variations targeting distinct genders:** Make two versions, one for each gender men and women.

**Instructions:**

- Do not use the words : young adults, elderly people, men, women, and the words that imply them,
to make the content very subtle and doesn't look like it is targeting that specific demographic group, the generated content must seem neutral.
- Craft each one with a headline and a short body text (without exceeding two lines) that persuades potential customers to engage with the its content.
- Tailor the language and content of each one to align with its respective audience.
- Aim for diversity in tone, language, and persuasive techniques across all variations.
- Ensure coherence and relevance with the provided article details and its content.
- Use arguments only from the source text that i provide you with.
- Do not exceed 50 characters in the headline, and do not exceed 125 character in the body.
- Adhere to Meta's guidelines of advertising, create headlines and bodys that do not require authorization or a disclaimer, the ads that need authorization and disclaimers are Ads about environmental politics, with ad content that includes discussion, debate and/or advocacy for or against topics, including but not limited to climate change, renewable/sustainable energy and fossil fuels, are subject to review and enforcement. Avoid formulating things similar to that, here are examples of ads that need authorization and a discplaimer:
"Going to the beach used to be fun, now all we see is waste plastics. We need environmental policy change now!"

"Fracking is ruining our community."

"How can we better tackle climate change?"
{article}''',height=800)
    # st.button("Generate", type="primary")
    if st.button("Generate") :
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(1, 101):
            progress_bar.progress(i)
            time.sleep(0.04)
        st.dataframe(row[["neutral","young_adults","elderly_people","men","women"]],hide_index=True)


# Evaluation 
st.markdown("# **Ad Evaluation**")
st.markdown("## **Diversity : BERTScore**")
st.markdown("### **Inter Group**")
if st.button("Calculate similarities") :
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        progress_bar.progress(i)
        time.sleep(0.03)
    data1 = {
    "Pair": ["Men-Women", "Young_adults-Elderly_people", "Neutral-Men", "Neutral-Women", "Neutral-Young_adults", "Neutral-Elderly_people"],
    "Score": [0.9251029, 0.88981426, 0.8890907, 0.87636423, 0.887433, 0.8565947]
    }
    st.dataframe(data1,hide_index=True)

st.markdown("### **Inter Topic**")
st.write(f"**Selected Articles** : {id} and a random article")
# articles=pd.DataFrame([df3.iloc[id].to_dict()])
if st.button("Calculate similarity") :
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        progress_bar.progress(i)
        time.sleep(0.03)
    data2={
        "Group": ["Elderly people","Young adults","Men","women"],
        "Score" :[ 0.8024446368217468,0.8292478322982788,0.8138522505760193, 0.8241235613822937]
    }
    st.dataframe(data2,hide_index=True)


st.markdown("## **Coherence : Our Solution**")
st.markdown("### **Claim Extraction : Gemini-1.5-Pro**")
if st.button("Extract Claims") :
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        progress_bar.progress(i)
        time.sleep(0.02)
    with open('../Data/ads_claims.json', 'r') as f:
        data = json.load(f)

    for article in data : 
        if article["articleId"]==id : 
            ads=article["ads"]

    claims=[]
    for ad in ads : 
        for claim in ad["claims"] : 
            claims.append({"Ad Type": ad["type"],"Ad Id":ad["id"],  "Ad Text":ad["adText"],"Claim Id":claim["claimId"], "Claim":claim["claimText"]})

    st.dataframe(claims,hide_index=True)


st.markdown("### **Natural Language Inference (NLI) :DeBERTa**")
if st.button("Calculate NLI Score"): 
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        progress_bar.progress(i)
        time.sleep(0.04)
    results=pd.read_csv("../Data/ads_claims_scores_dg.csv")
    row=results[results['articleId'] == id]
    # row=row[["articleId","adId","claimId","entailment","neutral","contradiction"]]
    st.markdown("**Used NLI equations**")
    st.latex(r'''
        \text{NLI\_1}=ent+neut-cont
    ''')
    st.latex(r'''
        \text{NLI\_2}=ent+cont
    ''')
    st.latex(r'''
        \text{NLI\_3}=max(ent,neut)
    ''')
    st.latex(r'''
        \text{NLI\_4}=(ent+neut)/2
    ''')
    row['NLI_1'] = row.apply(lambda row: row['entailment'] + row['neutral'] - row['contradiction'], axis=1)


    # score 2 : e-c
    row['NLI_2'] = row.apply(lambda row: row['entailment'] - row['contradiction'], axis=1)

    # score 3 : max(e,n)
    row['NLI_3'] = row.apply(lambda row: row['entailment'] if (row['entailment']>row['neutral']) else row['neutral'], axis=1)

    #  score 4 : avg(e,n)
    row['NLI_4'] = row.apply(lambda row: (row['entailment'] + row['neutral'])/2 , axis=1)

    st.dataframe(row[["articleId","adId","claimId","entailment","neutral","contradiction"]],hide_index=True)