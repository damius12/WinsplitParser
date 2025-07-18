import numpy as np
import pandas as pd
import altair as alt
from main import main
import streamlit as st
from AltairCharts import AltairCharts

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
    if "number_features" not in st.session_state:
        st.session_state.number_features = 2
    if not st.session_state.control_survey_spec:
        st.markdown(event_data["date"])
        st.subheader(event_data["name"])
        st.markdown(event_data["class"])
        "---"

        half, other = st.columns(2, gap="medium")
        with half:
            "Would you like to add the techical and/or physical features of this race's controls?"
            "You can characterize each control through a custom set of criteria in order to gain a more tailored analysis!"
            left, right = st.columns(2)
            if left.button(
                "add extra feature", type="secondary", use_container_width=True
            ):
                st.session_state.number_features += 1
                st.rerun()
            if st.session_state.number_features > 0 and right.button(
                "remove one feature", type="tertiary", use_container_width=True
            ):
                st.session_state.number_features -= 1
                st.rerun()

            "Don't worry, you can skip this part:)"

            if st.button("skip", use_container_width=True):
                st.session_state.skip = True

        with other:
            st.subheader("Custom features")
            number_controls = len(raw[0]["splits"])
            number_features = st.session_state.number_features

            tab = [1] * (number_controls + 1)
            features_names = [1] * number_features

            features_matrix = np.zeros((number_controls, number_features))
            with st.container(border=True):
                for i in range(number_controls):
                    tab[i] = st.columns(number_features + 1)
                    if i > 0:
                        tab[i][0].markdown(i)
                    else:
                        tab[i][0].markdown("Control")
                    for f in range(number_features):
                        if i > 0:
                            features_matrix[i, f] = tab[i][f + 1].number_input(
                                "insert number",
                                min_value=-4,
                                max_value=4,
                                label_visibility="collapsed",
                                key=f"{i}-{f}",
                                step=1,
                            )
                        else:
                            features_names[f] = tab[i][f + 1].text_input(
                                "insert feature",
                                key=f,
                                placeholder="e. g.: climb, vegetation, runnability, tiredness, etc.",
                                label_visibility="collapsed",
                            )

            if "" in features_names:
                st.warning("to proceed all fields must be filled")

            if st.button(
                "**proceed**",
                type="primary",
                use_container_width=True,
                disabled="" in features_names,
            ):
                features = pd.DataFrame(
                    {
                        name: features_matrix[:, i]
                        for i, name in enumerate(features_names)
                    }
                )
                st.session_state.features = features
                st.session_state.control_survey_spec = True
                st.rerun()

if st.session_state.data_fetched and (
    st.session_state.control_survey_spec or st.session_state.skip
):

    features = st.session_state.features
    features_names = list(features.columns)
    display_features = []

    with st.sidebar:
        st.subheader(event_data["name"])
        event_data["class"]
        "---"
        personal_position = st.number_input("rank position", 1, len(raw))
        personal_name = raw[personal_position - 1]["name"]
        st.markdown(f"**{personal_name}**")
        "---"
        st.subheader("show gap")
        show_gap = st.radio(
            "show gap", ["absolute", "relative"], label_visibility="collapsed"
        )
        st.subheader("display features")
        for name in features_names:
            if st.checkbox(name, value=True):
                display_features.append(name)

    df = pd.DataFrame()
    df[display_features] = features[display_features]
    results = pd.DataFrame(raw[personal_position - 1]["splits"])
    df["gap"] = results["split_gap"]
    df["perc"] = results["percentage_gap"]
    df = df.drop(index=len(df) - 1)
    for i in df.index:
        df.at[i, "control"] = i + 1

    y = "gap" if show_gap == "absolute" else "perc"
    y_label = "s" if show_gap == "absolute" else "%"
    color_scale = alt.Scale(
        domain=[0, 25, 100, 300], range=["green", "yellow", "red", "darkred"]
    )

    H = 200

    splits = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("control:O", title=None),
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
            tooltip=[
                alt.Tooltip(field="control"),
                alt.Tooltip(field="gap", title="seconds gap", format=".0f"),
                alt.Tooltip(field="perc", title="%", format=".1f"),
            ],
        )
    ).properties(height=H)

    chart = splits
    for feature in display_features:
        base = AltairCharts(
            y_title=feature,
            x_label_visibility=False,
            plot_h=H * 2 / 5,
            small=8,
            medium=12,
        )
        axis = base.axis_ruler(df, color="blue")
        bars = base.data_chart("bar", df, "control:O", feature, "control").encode(
            color=alt.value("blue"),
            y=alt.Y(
                feature,
                axis=alt.Axis(titleFontSize=12, labelFontSize=8, title=feature),
                scale=alt.Scale(domain=[-4, 4]),
            ),
        )
        chart = chart & base.main_plot(bars, axis)

    st.altair_chart(chart)
