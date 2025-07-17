import numpy as np
import pandas as pd
import altair as alt
from main import main
import streamlit as st
from AltairCharts import AltairCharts

# https://obasen.orientering.se/winsplits/online/en/default.asp?page=table&databaseId=106316&categoryId=1

st.set_page_config(layout="wide")

if "raw" not in st.session_state:
    url = st.text_input("insert winsplit url")
    if st.button("fetch split times"):
        st.session_state.raw = main(
            url,
            [],
            False,
            [],
            5,
            "else",
        )
event_data = st.session_state.raw["event_data"]
raw = st.session_state.raw["results"]

with st.sidebar:
    st.subheader(event_data["name"])
    event_data["class"]
    "---"
    personal_position = st.number_input("rank position", 1, len(raw))
    personal_name = raw[personal_position - 1]["name"]
    st.markdown(f"**{personal_name}**")
    "---"
    show_gap = st.radio("show gap", ["absolute", "relative"])

df = pd.DataFrame()

results = pd.DataFrame(raw[personal_position - 1]["splits"])
df["gap"] = results["split_gap"]
df["perc"] = results["percentage_gap"]
df = df.drop(index=len(df) - 1)
for i in df.index:
    df.at[i, "control"] = i + 1

y = "gap" if show_gap == "absolute" else "perc"
y_label = "s" if show_gap == "absolute" else "%"
color_scale = alt.Scale(
    domain=[0, 50, 100, 300], range=["green", "yellow", "red", "darkred"]
)
altair = AltairCharts()
bars = altair.data_chart("bar", df, "control:O", y, "perc:Q").encode(
    y=(
        alt.Y(
            y,
            title=y_label,
            scale=(
                alt.Scale(domain=[0, np.ceil(max(df["perc"]) / 100) * 100])
                if show_gap == "relative"
                else alt.Undefined
            ),
        )
    ),
    color=alt.Color("perc:Q", scale=color_scale, title="percentage gap"),
)

st.altair_chart(bars)
