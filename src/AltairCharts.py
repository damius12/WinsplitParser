import pandas as pd
import altair as alt
from typing import Dict, Literal


class AltairCharts:

    def __init__(
        self,
        large: int = 22,
        medium: int = 18,
        small: int = 14,
        plot_w: int = 1200,
        plot_h: int = 340,
        x_title: str | None = None,
        y_title: str | None = None,
        leg_title: str | None = None,
        **kwargs,
    ):

        # sizes
        self.large = large  # legend title size
        self.medium = medium  # font axis titles and legend items size
        self.small = small  # font axis labels size
        self.plot_w = plot_w  # plot width
        self.plot_h = plot_h  # plot height

        # axes and legend
        self.x_title = x_title
        self.y_title = y_title
        self.leg_title = leg_title
        self.x_axis = alt.Axis(
            orient="bottom",
            titleFontSize=self.medium,
            labelFontSize=self.small,
            title=self.x_title,
            labelAngle=kwargs["x_label_angle"] if "x_label_angle" in kwargs else 0,
            format=(
                kwargs["x_label_format"]
                if "x_label_format" in kwargs
                else alt.Undefined
            ),
            labels=(
                kwargs["x_label_visibility"]
                if "x_label_visibility" in kwargs
                else alt.Undefined
            ),
        )
        self.y_axis = alt.Axis(
            titleFontSize=self.medium, labelFontSize=self.small, title=self.y_title
        )
        self.legend = alt.Legend(
            title=self.leg_title,
            titleFontSize=self.large,
            labelFontSize=self.medium,
            orient="top",
        )

    # SELECTIONS
    def legend_selection(self, field: list[str]):
        legend_sel = alt.selection_point(
            fields=field, bind="legend", empty=False, name="lgselection"
        )
        return legend_sel

    horizontal_zoom = alt.selection_interval(
        encodings=["x"], bind="scales", name="zoom"
    )
    abscissa_selection = alt.selection_point(
        on="mousemove",
        nearest=True,
        empty=False,
        encodings=["x"],
        clear="mouseout",
        name="xselection",
    )

    def data_chart(
        self,
        mark: Literal["line", "point", "area", "bar"],
        df: pd.DataFrame,
        x_series: str,
        y_series: str,
        color_series: str,
        line_w: float = 2,
        color_list: list = [],
        points: bool = False,
        lines: bool = False,
        **kwargs,
    ) -> alt.Chart:

        chart = alt.Chart(df).encode(
            x=alt.X(x_series, axis=self.x_axis),
            y=alt.Y(y_series, axis=self.y_axis),
            color=alt.Color(
                color_series,
                scale=(
                    alt.Scale(
                        domain=df[color_series].unique().tolist(),
                        range=color_list,
                    )
                    if color_list != []
                    else alt.Undefined
                ),
                legend=self.legend,
            ),
        )

        kw_interpolate = kwargs["interpolate"] if "interpolate" in kwargs else "linear"
        kw_opacity = kwargs["opacity"] if "opacity" in kwargs else 1

        if mark == "point":
            chart = chart.mark_point(opacity=kw_opacity)
        elif mark == "area":
            chart = chart.mark_area(
                point=points,
                line=lines,
                opacity=kw_opacity,
                interpolate=kw_interpolate,
            )
        elif mark == "line":
            chart = chart.mark_line(
                point=points,
                strokeWidth=line_w,
                opacity=kw_opacity,
                interpolate=kw_interpolate,
                strokeDash=kwargs["dash"] if "dash" in kwargs else alt.Undefined,
            )
        else:
            chart = chart.mark_bar(opacity=kw_opacity)

        return chart

    def vertical_ruler_with_tooltip(
        self,
        df: pd.DataFrame,
        x_series: str,
        tooltip_dict: Dict[str, list[str]] = {},
        visible: bool = True,
        color: str = "black",
        width: float = 0.3,
    ):

        tooltip_points = (
            alt.Chart(df)
            .mark_point(opacity=0)
            .encode(
                x=x_series,
                tooltip=(
                    [
                        alt.Tooltip(
                            key,
                            title=tooltip_dict[key][0],
                            format=(
                                tooltip_dict[key][1]
                                if len(tooltip_dict[key]) > 1
                                else alt.Undefined
                            ),
                        )
                        for key in tooltip_dict.keys()
                    ]
                    if tooltip_dict != {}
                    else alt.Undefined
                ),
            )
        ).add_params(self.abscissa_selection)

        ruler = (
            alt.Chart(df)
            .mark_rule(color=color, opacity=(1 if visible else 0), strokeWidth=width)
            .encode(x=x_series)
            .transform_filter(self.abscissa_selection)
        )

        chart = ruler + tooltip_points

        return chart

    def axis_ruler(
        self,
        df: pd.DataFrame,
        axis: Literal["x", "y"] = "x",
        color: str = "black",
        line_w: float = 0.4,
    ):
        ruler = alt.Chart(df).mark_rule(color=color, size=line_w)
        if axis == "x":
            line = ruler.encode(y=alt.datum(0))
        else:
            line = ruler.encode(x=alt.datum(0))

        return line

    def highlight_dots(
        self,
        df: pd.DataFrame,
        x_series: str,
        y_series: str,
        color_series: str,
        size: int = 100,
    ):

        dots = (
            alt.Chart(df)
            .mark_point(opacity=0.6, filled=True, size=size)
            .encode(
                x=x_series,
                y=y_series,
                color=color_series,
            )
            .transform_filter(self.abscissa_selection)
        )

        return dots

    def main_plot(
        self,
        *args: alt.LayerChart | alt.Chart,
        double_scale: bool = False,
    ) -> alt.LayerChart | alt.Chart:
        base = alt.Chart(pd.DataFrame()).mark_point().encode()
        for layer in args:
            base = base + layer
        chart = base.properties(width=self.plot_w, height=self.plot_h).resolve_scale(
            x="shared", y="independent" if double_scale else "shared"
        )
        return chart
