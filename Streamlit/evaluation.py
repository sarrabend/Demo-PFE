import pandas as pd 
import streamlit as st 
import matplotlib as plt 
import plotly.graph_objects as go

st.title("Evaluation of the Generated Data (Informational Ads - Demographic Groups)")

data=pd.read_csv("../Data/ads_claims_scores_dg.csv")

criteria=st.sidebar.radio("Choose the evaluation criteria",
                ["Diversity","Coherence"]
                 )

if criteria == "Diversity" : 
    st.markdown("## Ads Diversity")
    axis=st.selectbox("Dimension",["Inter Group","Inter Topic"])
    if axis == "Inter Group" : 
        st.markdown("### Inter Group Similarity Scores")
        ig=pd.read_csv("../Data/bert_score_inter_type_dg.csv")
        men_women=ig[ig["pair"]=="men-women"]["bertscore"]
        elderly_young=ig[ig["pair"]=="young_adults-elderly_people"]["bertscore"]
        neutral_women=ig[ig["pair"]=="neutral-women"]["bertscore"]
        neutral_men=ig[ig["pair"]=="neutral-men"]["bertscore"]
        neutral_elderly=ig[ig["pair"]=="neutral-elderly_people"]["bertscore"]
        neutral_young=ig[ig["pair"]=="neutral-young_adults"]["bertscore"]
        # Add box plot for entailment
        fig = go.Figure()
        fig.add_trace(go.Box(y=men_women, name="men-women", marker_color='#00A4CC'))
        fig.add_trace(go.Box(y=elderly_young, name='young_adults-elderly_people', marker_color='#FFB74D'))
        fig.add_trace(go.Box(y=neutral_women, name='neutral-women', marker_color='#8E24AA'))
        fig.add_trace(go.Box(y=neutral_men, name='neutral-men', marker_color='#0097A0'))
        fig.add_trace(go.Box(y=neutral_elderly, name='neutral-elderly_people', marker_color='#880E4F'))
        fig.add_trace(go.Box(y=neutral_young, name='neutral-young_adults', marker_color='#ff8f00'))
        
        # Update layout for the box plot
        fig.update_layout(
            title='Distribution of BERT similarity scores between different ad pairs (Ad types)',
            yaxis_title='Scores',
            xaxis_title='Pairs',
            boxmode='group'  # Group the box plots together for comparison
        )

        # Display the box plot in Streamlit
        st.plotly_chart(fig)
    elif axis=="Inter Topic" : 
        st.markdown("### Inter Group Similarity Scores")
        men=pd.read_csv("../Data/bert_similarity_scores_inter_topic_m.csv")["score"]
        women=pd.read_csv("../Data/bert_similarity_scores_inter_topic_w.csv")["score"]
        young=pd.read_csv("../Data/bert_similarity_scores_inter_topic_ya.csv")["score"]
        elderly=pd.read_csv("../Data/bert_similarity_scores_inter_topic_ep.csv")["score"]
        fig = go.Figure()
        fig.add_trace(go.Box(y=men, name="Men", marker_color='#00A4CC'))
        fig.add_trace(go.Box(y=women, name='Women', marker_color='#FFB74D'))
        fig.add_trace(go.Box(y=young, name='Young Adults', marker_color='#8E24AA'))
        fig.add_trace(go.Box(y=elderly, name='Elderly People', marker_color='#0097A0'))
    
        # Update layout for the box plot
        fig.update_layout(
            title='Distribution of BERT similarity scores of ads from different topics targeting the same group',
            yaxis_title='Scores',
            xaxis_title='Group',
            boxmode='group'  # Group the box plots together for comparison
        )

        # Display the box plot in Streamlit
        st.plotly_chart(fig)
elif criteria == "Coherence" :
    st.markdown("## Ads Coherence")
    st.dataframe(data,hide_index=True)
    # Creating a stacked bar plot

    # Concatenate articleId, adId, and claimId to form a unique identifier for each claim
    data['claim_ids'] = data['articleId'].astype(str) + '_' + data['adId'].astype(str) + '_' + data['claimId'].astype(str)
    data['ad_ids'] = data['articleId'].astype(str) + '_' + data['adId'].astype(str) 
    data['NLI_1'] = data.apply(lambda data: data['entailment'] + data['neutral'] - data['contradiction'], axis=1)


    # score 2 : e-c
    data['NLI_2'] = data.apply(lambda data: data['entailment'] - data['contradiction'], axis=1)

    # score 3 : max(e,n)
    data['NLI_3'] = data.apply(lambda data: data['entailment'] if (data['entailment']>data['neutral']) else data['neutral'], axis=1)

    #  score 4 : avg(e,n)
    data['NLI_4'] = data.apply(lambda data: (data['entailment'] + data['neutral'])/2 , axis=1)
    
    st.markdown("### NLI probabilities per Claim")
    sampled_data=data.head(150)
    # Data preparation for plotting
    claim_ids = sampled_data['claim_ids']  # Use the concatenated ids
    entailment = sampled_data['entailment']
    neutral = sampled_data['neutral']
    contradiction = sampled_data['contradiction']

    # Creating the figure
    fig = go.Figure()

    # Add entailment, neutral, and contradiction as stacked bars
    fig.add_trace(go.Bar(x=claim_ids, y=entailment, name='Entailment', marker_color='#0097A7'))
    fig.add_trace(go.Bar(x=claim_ids, y=neutral, name='Neutral', marker_color='#ff8f00'))
    fig.add_trace(go.Bar(x=claim_ids, y=contradiction, name='Contradiction', marker_color='#880E4F'))

    # Update layout for stacked bars
    fig.update_layout(
        barmode='stack',
        xaxis_title='Claim ID',
        yaxis_title='Percentage',
        title='Entailment, Neutral, and Contradiction Scores per Claim',
        showlegend=True
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### NLI scores")
    level = st.selectbox("Level",["Claim","Ad"])
    if level == "Claim" : 
        sampled=data.head(200)
        claim_ids = sampled['claim_ids']  # Use the concatenated ids
        nli = sampled['NLI_1']

        # Creating the figure
        fig = go.Figure()

        # Add entailment, neutral, and contradiction as stacked bars
        fig.add_trace(go.Bar(x=claim_ids, y=nli, name='NLI', marker_color='#0097A7'))

        # Update layout for stacked bars
        fig.update_layout(
            barmode='stack',
            xaxis_title='Claim ID',
            yaxis_title='Score',
            title='NLI Scores per Claim',
            showlegend=True
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig,use_container_width=True)
    elif level == "Ad" :
        ad_ids = data['ad_ids']  # Use the concatenated ids
        nli = data.groupby(["ad_ids"])['NLI_1'].mean()

        # Creating the figure
        fig = go.Figure()

        # Add entailment, neutral, and contradiction as stacked bars
        fig.add_trace(go.Bar(x=claim_ids, y=nli, name='NLI', marker_color='#0097A7'))

        # Update layout for stacked bars
        fig.update_layout(
            barmode='stack',
            xaxis_title='Claim ID',
            yaxis_title='Score',
            title='NLI Scores per Claim',
            showlegend=True
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig,use_container_width=True)


    st.markdown("### Coherence Rate")
    # Creating the pie chart
    fig = go.Figure(
        go.Pie(
            labels=['Coherent', 'Incoherent'],
            values=[93.1,6.9],
            marker=dict(colors=['#0097A7', '#FF8F00'])
        )
    )

    # Update layout for the pie chart
    fig.update_layout(
        title='Overall Coherence of the generated Ads',
    )
    st.plotly_chart(fig)

else : 
    st.write('Please choose a criteria')
