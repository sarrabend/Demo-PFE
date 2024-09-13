import opendatasets as od

import pathlib
import textwrap
import pandas as pd
import getpass
import os
import plotly.express as px
import csv







# Define a function to get a random sample of approximately 10% of items from each group
def get_random_sample(group):
    total_products = len(group)
    if total_products > 500 :
        return group.sample(500)
    else :
        return group

# od.download('https://www.kaggle.com/datasets/beridzeg45/guardian-environment-related-news?resource=download')

df=pd.read_csv("guardian-environment-related-news\guardian_environment_news.csv")
df=df.head(100)
df.to_csv("Data/news.csv")


# od.download('https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset?resource=download',force=True)


df=pd.read_csv("amazon-products-dataset\Amazon-Products.csv")

# Apply the function to each group (Category, Subcategory)
products_df = df.groupby(['main_category', 'sub_category']).apply(get_random_sample).reset_index(drop=True)



products_df=products_df.head(100)
products_df.to_csv("Data/products.csv",index=False)


