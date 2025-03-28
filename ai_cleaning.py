import pandas as pd
from word2number import w2n
from datetime import datetime

def convert_words_to_numbers(val):
    try:
        return w2n.word_to_num(str(val))
    except:
        return val

def ai_cleaning(df):
    log = []
    df_cleaned = df.copy()

    for col in df.columns:
        col_lower = col.lower()
        if "email" in col_lower:
            df_cleaned = df_cleaned[df_cleaned[col].str.contains('@', na=False)]
            log.append(f"✅ Cleaned invalid emails in: {col}")
        elif "age" in col_lower:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
            df_cleaned = df_cleaned[df_cleaned[col].between(10, 100)]
            log.append(f"📊 Filtered out invalid ages in: {col}")
        elif "salary" in col_lower:
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(r"[$,]", "", regex=True)
            df_cleaned[col] = df_cleaned[col].apply(convert_words_to_numbers)
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
            log.append(f"💰 Cleaned currency/text in: {col}")
        elif "date" in col_lower or "join" in col_lower:
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
            df_cleaned = df_cleaned.dropna(subset=[col])
            log.append(f"📅 Cleaned dates in: {col}")
        else:
            df_cleaned[col] = df_cleaned[col].fillna("Unknown")

    log.append(f"✅ Final cleaned shape: {df_cleaned.shape}")
    return df_cleaned, log