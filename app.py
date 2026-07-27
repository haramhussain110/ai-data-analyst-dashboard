import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import os 
from dotenv import load_dotenv
from openai import OpenAI

def clean_data(df):
    df= df.copy()

    before =df.shape[0]
    df= df.drop_duplicates()
    after = df.shape[0]
    duplicates_removed = before-after
    # print(f"removed{before - after}Duplicated Row")

    numeric_column = df.select_dtypes(include=[np.number]).columns
    for col in numeric_column:
        if df[col].isnull().sum() >0:
            median_val = df[col].median()
            df[col]= df[col].fillna(median_val)
            # print(f"fill missing value {col}with median:{median_val}")

    text_column =df.select_dtypes(include=["object"]).columns

    for col in text_column:
        if df[col].isnull().sum() >0:
            df[col] =df[col].fillna("unknown")
            # print(f"Filled missng category{col}wirh unknown ")
    return df ,duplicates_removed



def generate_ai_summary(df,testing_mode=True):
    stats_text=f"""Dataset shape: {df.shape[0]} rows,{df.shape[1]} columns
    columns List:{list(df.columns)}
    Numeric Summary:
    {df.describe().to_string()}
    Region Distribution:
    {df["Region"].value_counts().to_string()}

    """

    if testing_mode:
        return "Mock summary :Real AI response will appear here"
    client =OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response =client.chat.completions.create(
        model= "gpt-4o-mini",
        max_tokens=500,
        messages=[
            {
            "role":"user",

            "content":f"You are a data analyst.Based on the following statistics,give a Business owner 4-5 clear,plain-English Bullet-point insights(no technical):\n\n{stats_text}"
            }
        ]
    )
    return response.choices[0].message.content

def export_to_excel(df_clean,summary,filename="report.xlsx"):
    with pd.ExcelWriter(filename,engine="openpyxl")as writer:
        df_clean.to_excel(writer,sheet_name="cleaned_Data",index=False)
        summary_df =pd.DataFrame({"AI Summary":[summary] })
        summary_df.to_excel(writer,sheet_name="AI_summary",index=False)

        worksheet =writer.sheets["AI_summary"]
        worksheet.column_dimensions["A"].width = 100
        from openpyxl.styles import Alignment
        worksheet["A2"].alignment =Alignment(wrap_text=True,vertical="top")
        worksheet.row_dimensions[2].height=200

    return filename





load_dotenv()


st.set_page_config(page_title= "AI Data Anayst Dashboard ",layout="wide")
st.title("AI Data Analyst Dashboard")
st.write("upload your CSV file and get instant cleaning ,charts and AI insights.")

uploaded_file = st.file_uploader("Upload CSV",type=["csv"])
if uploaded_file is not None:
    df =pd.read_csv(uploaded_file)

    st.success(f"File uplaoded ! shape:{df.shape[0]}rows ,{df.shape[1]}columns ")
    st.dataframe(df.head())

    df_clean ,duplicates_removed =clean_data(df)
    st.info(f"Cleaned! Removed{duplicates_removed} duplicate rows .Missing value filled ")
    st.dataframe(df_clean.head())

    st.subheader("Price Distribution")
    fig1,ax1 =plt.subplots(figsize=(5,3))
    sns.histplot(df_clean["Price"],bins=20,kde=True,ax=ax1)
    ax1.set_title("Price Distribution")
    st.pyplot(fig1,use_container_width=False) 

    st.subheader("Orders by Region")
    fig2,ax2 =plt.subplots(figsize=(5,3))
    df_clean["Region"].value_counts().plot(kind='bar',color='skyblue',edgecolor='black',ax=ax2)
    ax2.set_title("Orders by Region")
    ax2.set_xlabel("Region")
    ax2.set_ylabel("count")
    st.pyplot(fig2,use_container_width=False)

    st.subheader("Correlation Heatemap ")
    fig3,ax3 = plt.subplots(figsize=(4,3))
    numeric_df  = df_clean.select_dtypes(include=[np.number])
    correlation = numeric_df.corr()
    sns.heatmap(correlation,annot=True,cmap="coolwarm",fmt=".2f",ax=ax3)
    ax3.set_title("correlation Heatmap")
    st.pyplot(fig3,use_container_width=False)


    st.subheader("AI summary")
    summary =generate_ai_summary(df_clean,testing_mode=True)
    st.write(summary)

    if st.button("Generate Excel Report "):
        filename = export_to_excel(df_clean,summary)
        with open(filename,"rb")as f:
            st.download_button(
                label="Download Excel Report",
                data=f,
                file_name="report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            )

