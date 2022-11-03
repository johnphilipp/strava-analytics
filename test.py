import streamlit as st
import pandas as pd
from utils.process_data import process_data
from utils import fig


# -----------------------------------------------
# Edit df
# -----------------------------------------------

st.write("# Calendar Tracker")
st.write("")

df = pd.read_json('data/activities.json')
df = process_data(df)

df_years_months = df['start_date_local'].str.split('-', expand=True)
df_years_months = df_years_months.rename(columns={df_years_months.columns[0]: 'year', df_years_months.columns[1]: 'month'})

df_days = df_years_months[2].str.split('T', expand=True)
df_days = df_days.rename(columns={df_days.columns[0]: 'day'})

df_years_months = df_years_months.iloc[: , :-1]
df_days = df_days.iloc[: , :-1]

df = pd.concat([df, df_years_months, df_days], axis=1, join="inner")
df = df.astype({'year':'int', 'month':'int', 'day':'int'})

year = st.selectbox("Select year", df["year"].unique().tolist())

df = df.loc[df['year'] == year]

st.write("")

# -----------------------------------------------
# Append images to df
# -----------------------------------------------

def add(row):
    df = row["summary_polyline"]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    figure = fig.line_fig(df)
    img = fig.get_img(figure)
    return img.read()

df['img'] = df.apply(add, axis=1)

# -----------------------------------------------
# Print images in df where day/month/year matches
# -----------------------------------------------

c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = st.columns(13)

img_width = 53
top = 4
bottom = 24.65

c0.write("\#")
for i in range(1, 32):
    text = str(i)
    html_str = f"""
    <p style="margin-top: {top}px; margin-bottom: {bottom}px;">{text}</p>
    """
    c0.markdown(html_str, unsafe_allow_html=True)

text = "-"
html_str = f"""
<p style="margin-top: {top}px; margin-bottom: {bottom}px;">{text}</p>
"""

c1.write("Jan")
df2 = df.loc[df['month'] == 1]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c1.image(img, width=img_width)
    else:
        c1.markdown(html_str, unsafe_allow_html=True)

c2.write("Feb")
df2 = df.loc[df['month'] == 2]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c2.image(img, width=img_width)
    else:
        c2.markdown(html_str, unsafe_allow_html=True)

c3.write("Mar")
df2 = df.loc[df['month'] == 3]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c3.image(img, width=img_width)
    else:
        c3.markdown(html_str, unsafe_allow_html=True)

c4.write("Apr")
df2 = df.loc[df['month'] == 4]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c4.image(img, width=img_width)
    else:
        c4.markdown(html_str, unsafe_allow_html=True)

c5.write("May")
df2 = df.loc[df['month'] == 5]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c5.image(img, width=img_width)
    else:
        c5.markdown(html_str, unsafe_allow_html=True)

c6.write("Jun")
df2 = df.loc[df['month'] == 6]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c6.image(img, width=img_width)
    else:
        c6.markdown(html_str, unsafe_allow_html=True)

c7.write("Jul")
df2 = df.loc[df['month'] == 7]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c7.image(img, width=img_width)
    else:
        c7.markdown(html_str, unsafe_allow_html=True)

c8.write("Aug")
df2 = df.loc[df['month'] == 8]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c8.image(img, width=img_width)
    else:
        c8.markdown(html_str, unsafe_allow_html=True)

c9.write("Sep")
df2 = df.loc[df['month'] == 9]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c9.image(img, width=img_width)
    else:
        c9.markdown(html_str, unsafe_allow_html=True)

c10.write("Oct")
df2 = df.loc[df['month'] == 10]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c10.image(img, width=img_width)
    else:
        c10.markdown(html_str, unsafe_allow_html=True)

c11.write("Nov")
df2 = df.loc[df['month'] == 11]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c11.image(img, width=img_width)
    else:
        c11.markdown(html_str, unsafe_allow_html=True)

c12.write("Dec")
df2 = df.loc[df['month'] == 12]
df2 = df2.reset_index()
unique = df2['day'].unique()
for i in range(1, 32):
    if i in unique:
        index = df2.index[df2['day'] == i].tolist()[0] # TODO: could be multiple activities per day
        img = fig.invert_colors_img(df2["img"].iloc[index])
        c12.image(img, width=img_width)
    else:
        c12.markdown(html_str, unsafe_allow_html=True)