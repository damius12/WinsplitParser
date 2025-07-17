import numpy as np
import pandas as pd
import altair as alt
from main import main
import streamlit as st
from AltairCharts import AltairCharts

# https://obasen.orientering.se/winsplits/online/en/default.asp?page=table&databaseId=106316&categoryId=1

st.set_page_config(layout="wide")

if "data_fetched" not in st.session_state:
    st.session_state.data_fetched = False
if "control_survey_spec" not in st.session_state:
    st.session_state.control_survey_spec = False
if "assign_features" not in st.session_state:
    st.session_state.assign_features = False
if "skip" not in st.session_state:
    st.session_state.skip = False

if not st.session_state.data_fetched:
    url = st.text_input("insert winsplit url")
    if st.button("fetch split times", disabled=url == ""):
        st.session_state.raw = main(
            url,
            [],
            False,
            [],
            5,
            "else",
        )
        st.session_state.data_fetched = True
        st.rerun()

else:
    event_data = st.session_state.raw["event_data"]
    raw = st.session_state.raw["results"]
    if "features_number" not in st.session_state:
        st.session_state.features_number = 1
    if not st.session_state.control_survey_spec:
        st.markdown(event_data["date"])
        st.subheader(event_data["name"])
        st.markdown(event_data["class"])
        "---"
        "Would you like to add the techical and/or physical features of this race's controls?"
        "You can characterize each control with a custom set of criteria in order to gain a more tailored analysis!"

        half, other = st.columns(2)
        with half:
            st.subheader("Custom features")
            features_names = [1] * st.session_state.features_number
            for i in range(0, st.session_state.features_number):
                features_names[i] = st.text_input(
                    f"insert a feature {i}",
                    placeholder="e. g.: climb, vegetation, runnability, tiredness, etc.",
                    label_visibility="collapsed",
                )
            left, right = st.columns(2)
            if left.button(
                "add extra feature", type="secondary", use_container_width=True
            ):
                st.session_state.features_number += 1
                st.rerun()
            if st.session_state.features_number > 0 and right.button(
                "remove one feature", type="tertiary", use_container_width=True
            ):
                st.session_state.features_number -= 1
                st.rerun()
            "you can assign values within a customized range:"
            feature_range = st.slider(
                "range",
                min_value=-10,
                max_value=10,
                value=(0, 5),
                label_visibility="collapsed",
            )
            "---"
            if "" in features_names:
                st.warning("to proceed all fields must be filled")
            yes, no = st.columns(2)
            if yes.button(
                "**proceed**",
                type="primary",
                use_container_width=True,
                disabled="" in features_names,
            ):
                st.session_state.features = features_names
                st.session_state.control_survey_spec = True
                st.rerun()
            if no.button("skip", use_container_width=True):
                st.session_state.control_survey_spec = True
                st.session_state.skip = True
    if st.session_state.control_survey_spec and not (
        st.session_state.assign_features or st.session_state.skip
    ):
        st.write(st.session_state.features)

if (
    st.session_state.data_fetched
    and st.session_state.control_survey_spec
    and (st.session_state.assign_features or st.session_state.skip)
):

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
