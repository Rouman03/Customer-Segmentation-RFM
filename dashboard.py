import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

st.title("Customer Segmentation Dashboard (RFM Analysis)")

conn = sqlite3.connect("database/retail.db")

query = """
SELECT
    [Customer ID] as CustomerID,
    MAX(InvoiceDate) as LastPurchase,
    COUNT(DISTINCT Invoice) as Frequency,
    SUM(TotalPrice) as Monetary
FROM transactions
GROUP BY [Customer ID]
"""

rfm = pd.read_sql(query, conn)
rfm['LastPurchase'] = pd.to_datetime(rfm['LastPurchase'])

today_date = rfm['LastPurchase'].max() + pd.Timedelta(days=1)
rfm['Recency'] = (today_date - rfm['LastPurchase']).dt.days

rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 4, labels=[1,2,3,4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + \
                   rfm['F_Score'].astype(str) + \
                   rfm['M_Score'].astype(str)

def segment(row):
    if row['RFM_Score'] == '444': return 'Best Customer'
    if row['R_Score'] == 4: return 'Recent Customer'
    if row['F_Score'] == 4: return 'Loyal Customer'
    return 'Others'

rfm['Segment'] = rfm.apply(segment, axis=1)

st.subheader("RFM Data Preview")
st.dataframe(rfm.head())


st.subheader("Customer Segment Distribution")
fig1, ax1 = plt.subplots()
rfm['Segment'].value_counts().plot(kind='bar', ax=ax1)
st.pyplot(fig1)


st.subheader("RFM Heatmap")
heatmap_data = rfm.groupby(['R_Score', 'F_Score'])['Monetary'].mean().unstack()

fig2, ax2 = plt.subplots()
sns.heatmap(heatmap_data, annot=True, fmt=".0f", ax=ax2)
st.pyplot(fig2)