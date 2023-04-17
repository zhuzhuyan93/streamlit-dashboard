import streamlit as st
from tools.assignCss import local_css
import os
import pandas as pd
from streamlit_echarts import st_echarts
from tools import echartsPlot
from tools.publicComponent import *
from streamlit_toggle import st_toggle_switch
from streamlit_elements import elements, dashboard, mui, nivo, html


def main():
    st.header("小专题")

    layout = [
        dashboard.Item("面积图", 0, 0, 5, 3),
        dashboard.Item("漏斗图", 0, 0, 4, 3),
        dashboard.Item("曲线图", 0, 2, 6, 3),
        dashboard.Item("柱状图", 6, 2, 6, 3),
        dashboard.Item("雷达图", 0, 4, 5, 4),
        dashboard.Item("饼图", 6, 4, 7, 4),
    ]

    with elements("demo"):
        # with mui.Paper:
        #     with mui.Typography:
        #         html.h1(
        #             "Streamlit-elements使用案例",
        #             css={
        #                 "backgroundColor": "transparent",
        #                 "color": "black",
        #                 "borderColor": "transparent",
        #                 # "borderRadius": "5px",
        #                 # "zIndex": "tooltip",
        #                 # "height": "45px",
        #                 # "&:hover": {"color": "lightgreen"},
        #             },
        #         )

        with dashboard.Grid(layout, draggableHandle=".draggable"):
            # with mui.Card(
            #     key="曲线图",
            #     sx={
            #         "color": "black",
            #         "bgcolor": "transparent",
            #         "display": "flex",
            #         # "borderRadius": 2,
            #         "flexDirection": "column",
            #     },
            # ):
            #     mui.CardHeader(title="曲线图", className="draggable")
            #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
            #
            #         data_quxian = [
            #             {
            #                 "id": "japan",
            #                 "color": "hsl(158, 70%, 50%)",
            #                 "data": [
            #                     {"x": "plane", "y": 44},
            #                     {"x": "helicopter", "y": 84},
            #                     {"x": "boat", "y": 57},
            #                     {"x": "train", "y": 89},
            #                     {"x": "subway", "y": 50},
            #                     {"x": "bus", "y": 26},
            #                     {"x": "car", "y": 46},
            #                 ],
            #             },
            #             {
            #                 "id": "france",
            #                 "color": "hsl(40, 70%, 50%)",
            #                 "data": [
            #                     {"x": "plane", "y": 70},
            #                     {"x": "helicopter", "y": 66},
            #                     {"x": "boat", "y": 44},
            #                     {"x": "train", "y": 73},
            #                     {"x": "subway", "y": 86},
            #                     {"x": "bus", "y": 89},
            #                     {"x": "car", "y": 29},
            #                 ],
            #             },
            #             {
            #                 "id": "norway",
            #                 "color": "hsl(99, 70%, 50%)",
            #                 "data": [
            #                     {"x": "plane", "y": 28},
            #                     {"x": "helicopter", "y": 70},
            #                     {"x": "boat", "y": 48},
            #                     {"x": "train", "y": 40},
            #                     {"x": "subway", "y": 29},
            #                     {"x": "bus", "y": 62},
            #                     {"x": "car", "y": 52},
            #                 ],
            #             },
            #         ]
            #         nivo.Bump(
            #             data=data_quxian,
            #             margin={"top": 50, "right": 110, "bottom": 50, "left": 60},
            #             xScale={"type": "point"},
            #             yScale={
            #                 "type": "linear",
            #                 "min": "auto",
            #                 "max": "auto",
            #                 "stacked": "true",
            #                 "reverse": "false",
            #             },
            #             yFormat=" >-.2f",
            #             axisTop={"null"},
            #             axisBottom={
            #                 "orient": "bottom",
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "transportation",
            #                 "legendOffset": 36,
            #                 "legendPosition": "middle",
            #             },
            #             axisLeft={
            #                 "orient": "left",
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "count",
            #                 "legendOffset": -40,
            #                 "legendPosition": "middle",
            #             },
            #             pointSize={10},
            #             pointColor={"theme": "background"},
            #             pointBorderWidth={2},
            #             pointBorderColor={"from": "serieColor"},
            #             pointLabelYOffset={-12},
            #             useMesh={"true"},
            #             legends=[
            #                 {
            #                     "anchor": "bottom-right",
            #                     "direction": "column",
            #                     "justify": "false",
            #                     "translateX": 100,
            #                     "translateY": 0,
            #                     "itemsSpacing": 0,
            #                     "itemDirection": "left-to-right",
            #                     "itemWidth": 80,
            #                     "itemHeight": 20,
            #                     "itemOpacity": 0.75,
            #                     "symbolSize": 12,
            #                     "symbolShape": "circle",
            #                     "symbolBorderColor": "rgba(0, 0, 0, .5)",
            #                     "effects": [
            #                         {
            #                             "on": "hover",
            #                             "style": {
            #                                 "itemBackground": "rgba(0, 0, 0, .03)",
            #                                 "itemOpacity": 1,
            #                             },
            #                         }
            #                     ],
            #                 }
            #             ],
            #             theme={
            #                 "background": "#00cccc",
            #                 "textColor": "white",
            #                 "tooltip": {
            #                     "container": {
            #                         "background": "#FFFFFF",
            #                         "color": "#31333F",
            #                     }
            #                 },
            #             },
            #         )
            #
            # with mui.Card(
            #     key="柱状图",
            #     sx={
            #         "color": "white",
            #         "bgcolor": "transparent",
            #         "display": "flex",
            #         "borderRadius": 2,
            #         "flexDirection": "column",
            #     },
            # ):
            #     mui.CardHeader(title="柱状图", className="draggable")
            #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
            #
            #         data_zhuzhuangtu = [
            #             {
            #                 "country": "AD",
            #                 "hot dog": 133,
            #                 "hot dogColor": "hsl(23, 70%, 50%)",
            #                 "burger": 54,
            #                 "burgerColor": "hsl(288, 70%, 50%)",
            #                 "sandwich": 98,
            #                 "sandwichColor": "hsl(182, 70%, 50%)",
            #                 "kebab": 157,
            #                 "kebabColor": "hsl(78, 70%, 50%)",
            #                 "fries": 97,
            #                 "friesColor": "hsl(246, 70%, 50%)",
            #                 "donut": 119,
            #                 "donutColor": "hsl(320, 70%, 50%)",
            #             },
            #             {
            #                 "country": "AE",
            #                 "hot dog": 35,
            #                 "hot dogColor": "hsl(51, 70%, 50%)",
            #                 "burger": 69,
            #                 "burgerColor": "hsl(330, 70%, 50%)",
            #                 "sandwich": 94,
            #                 "sandwichColor": "hsl(110, 70%, 50%)",
            #                 "kebab": 99,
            #                 "kebabColor": "hsl(281, 70%, 50%)",
            #                 "fries": 166,
            #                 "friesColor": "hsl(245, 70%, 50%)",
            #                 "donut": 14,
            #                 "donutColor": "hsl(277, 70%, 50%)",
            #             },
            #             {
            #                 "country": "AF",
            #                 "hot dog": 48,
            #                 "hot dogColor": "hsl(337, 70%, 50%)",
            #                 "burger": 115,
            #                 "burgerColor": "hsl(49, 70%, 50%)",
            #                 "sandwich": 95,
            #                 "sandwichColor": "hsl(337, 70%, 50%)",
            #                 "kebab": 93,
            #                 "kebabColor": "hsl(115, 70%, 50%)",
            #                 "fries": 91,
            #                 "friesColor": "hsl(169, 70%, 50%)",
            #                 "donut": 171,
            #                 "donutColor": "hsl(301, 70%, 50%)",
            #             },
            #         ]
            #         nivo.Bar(
            #             data=data_zhuzhuangtu,
            #             layout="horizontal",
            #             keys=[
            #                 "hot dog",
            #                 "burger",
            #                 "sandwich",
            #                 "kebab",
            #                 "fries",
            #                 "donut",
            #             ],
            #             indexBy="country",
            #             margin={"top": 20, "right": 130, "bottom": 50, "left": 60},
            #             padding={0.4},
            #             valueScale={"type": "linear"},
            #             indexScale={"type": "band", "round": "true"},
            #             colors={"scheme": "nivo"},
            #             borderColor={"from": "color", "modifiers": [["darker", 1.6]]},
            #             axisTop={"null"},
            #             axisBottom={
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "country",
            #                 "legendPosition": "middle",
            #                 "legendOffset": 32,
            #             },
            #             axisLeft={
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "food",
            #                 "legendPosition": "middle",
            #                 "legendOffset": -40,
            #             },
            #             labelSkipWidth={12},
            #             labelSkipHeight={12},
            #             labelTextColor={
            #                 "from": "color",
            #                 "modifiers": [["darker", 1.6]],
            #             },
            #             legends=[
            #                 {
            #                     "dataFrom": "keys",
            #                     "anchor": "top-right",
            #                     "direction": "column",
            #                     "margin": {"left": 10},
            #                     "justify": "false",
            #                     "translateX": 120,
            #                     "translateY": 0,
            #                     "itemsSpacing": 2,
            #                     "itemWidth": 100,
            #                     "itemHeight": 20,
            #                     "itemDirection": "left-to-right",
            #                     "itemOpacity": 0.85,
            #                     "symbolSize": 20,
            #                     "effects": [
            #                         {"on": "hover", "style": {"itemOpacity": 1}}
            #                     ],
            #                 }
            #             ],
            #             theme={
            #                 "background": "#00cccc",
            #                 "textColor": "white",
            #                 "tooltip": {
            #                     "container": {
            #                         "background": "#FFFFFF",
            #                         "color": "#31333F",
            #                     }
            #                 },
            #             },
            #             role="application",
            #             ariaLabel="Nivo bar chart demo",
            #         )
            #
            # with mui.Card(
            #     key="雷达图",
            #     sx={
            #         "color": "white",
            #         "bgcolor": "primary.main",
            #         "display": "flex",
            #         "borderRadius": 2,
            #         "flexDirection": "column",
            #     },
            # ):
            #     mui.CardHeader(title="雷达图", className="draggable")
            #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
            #
            #         data_leida = [
            #             {
            #                 "taste": "fruity",
            #                 "chardonay": 93,
            #                 "carmenere": 61,
            #                 "syrah": 114,
            #             },
            #             {
            #                 "taste": "bitter",
            #                 "chardonay": 91,
            #                 "carmenere": 37,
            #                 "syrah": 72,
            #             },
            #             {
            #                 "taste": "heavy",
            #                 "chardonay": 56,
            #                 "carmenere": 95,
            #                 "syrah": 99,
            #             },
            #             {
            #                 "taste": "strong",
            #                 "chardonay": 64,
            #                 "carmenere": 90,
            #                 "syrah": 30,
            #             },
            #             {
            #                 "taste": "sunny",
            #                 "chardonay": 119,
            #                 "carmenere": 94,
            #                 "syrah": 103,
            #             },
            #         ]
            #
            #         nivo.Radar(
            #             data=data_leida,
            #             keys=["chardonay", "carmenere", "syrah"],
            #             indexBy="taste",
            #             valueFormat=">-.2f",
            #             margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
            #             borderColor={"from": "color"},
            #             gridLabelOffset=36,
            #             dotSize=10,
            #             dotColor={"theme": "background"},
            #             dotBorderWidth=2,
            #             motionConfig="wobbly",
            #             legends=[
            #                 {
            #                     "anchor": "top-left",
            #                     "direction": "column",
            #                     "translateX": -50,
            #                     "translateY": -40,
            #                     "itemWidth": 80,
            #                     "itemHeight": 20,
            #                     "itemTextColor": "#999",
            #                     "symbolSize": 12,
            #                     "symbolShape": "circle",
            #                     "effects": [
            #                         {"on": "hover", "style": {"itemTextColor": "#000"}}
            #                     ],
            #                 }
            #             ],
            #             theme={
            #                 "background": "#00cccc",
            #                 "textColor": "white",
            #                 "tooltip": {
            #                     "container": {
            #                         "background": "#FFFFFF",
            #                         "color": "#31333F",
            #                     }
            #                 },
            #             },
            #         )
            #
            # with mui.Card(
            #     key="饼图",
            #     sx={
            #         "color": "white",
            #         "bgcolor": "primary.main",
            #         "display": "flex",
            #         "borderRadius": 2,
            #         "flexDirection": "column",
            #     },
            # ):
            #     mui.CardHeader(title="饼图", className="draggable")
            #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
            #
            #         data_bingtu = [
            #             {
            #                 "id": "erlang",
            #                 "label": "erlang",
            #                 "value": 81,
            #                 "color": "hsl(111, 70%, 50%)",
            #             },
            #             {
            #                 "id": "sass",
            #                 "label": "sass",
            #                 "value": 542,
            #                 "color": "hsl(345, 70%, 50%)",
            #             },
            #             {
            #                 "id": "haskell",
            #                 "label": "haskell",
            #                 "value": 537,
            #                 "color": "hsl(172, 70%, 50%)",
            #             },
            #             {
            #                 "id": "css",
            #                 "label": "css",
            #                 "value": 98,
            #                 "color": "hsl(145, 70%, 50%)",
            #             },
            #             {
            #                 "id": "hack",
            #                 "label": "hack",
            #                 "value": 515,
            #                 "color": "hsl(281, 70%, 50%)",
            #             },
            #         ]
            #
            #         nivo.Pie(
            #             data=data_bingtu,
            #             margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
            #             innerRadius={0.5},
            #             cornerRadius={6},
            #             padAngle={0.7},
            #             activeOuterRadiusOffset={8},
            #             borderWidth={1},
            #             borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
            #             arcLinkLabelsSkipAngle={10},
            #             arcLinkLabelsTextColor="#333333",
            #             arcLinkLabelsThickness={2},
            #             arcLinkLabelsColor={"from": "color"},
            #             arcLabelsSkipAngle={10},
            #             arcLabelsTextColor={
            #                 "from": "color",
            #                 "modifiers": [["darker", 2]],
            #             },
            #             legends=[
            #                 {
            #                     "anchor": "top-left",
            #                     "direction": "column",
            #                     "translateX": -50,
            #                     "translateY": -40,
            #                     "itemWidth": 80,
            #                     "itemHeight": 20,
            #                     "itemTextColor": "#999",
            #                     "symbolSize": 12,
            #                     "symbolShape": "circle",
            #                     "effects": [
            #                         {"on": "hover", "style": {"itemTextColor": "#000"}}
            #                     ],
            #                 }
            #             ],
            #             theme={
            #                 "background": "#00cccc",
            #                 "textColor": "white",
            #                 "tooltip": {
            #                     "container": {
            #                         "background": "#FFFFFF",
            #                         "color": "#31333F",
            #                     }
            #                 },
            #             },
            #         )
            #
            # with mui.Card(
            #     key="面积图",
            #     sx={
            #         "color": "white",
            #         "bgcolor": "primary.main",
            #         "display": "flex",
            #         "borderRadius": 2,
            #         "flexDirection": "column",
            #     },
            # ):
            #     mui.CardHeader(title="面积图", className="draggable")
            #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
            #
            #         data_area = [
            #             {
            #                 "Raoul": 168,
            #                 "Josiane": 148,
            #                 "Marcel": 149,
            #                 "René": 109,
            #                 "Paul": 163,
            #                 "Jacques": 95,
            #             },
            #             {
            #                 "Raoul": 189,
            #                 "Josiane": 145,
            #                 "Marcel": 133,
            #                 "René": 194,
            #                 "Paul": 115,
            #                 "Jacques": 96,
            #             },
            #             {
            #                 "Raoul": 33,
            #                 "Josiane": 189,
            #                 "Marcel": 145,
            #                 "René": 171,
            #                 "Paul": 178,
            #                 "Jacques": 177,
            #             },
            #             {
            #                 "Raoul": 109,
            #                 "Josiane": 49,
            #                 "Marcel": 10,
            #                 "René": 37,
            #                 "Paul": 169,
            #                 "Jacques": 120,
            #             },
            #             {
            #                 "Raoul": 28,
            #                 "Josiane": 133,
            #                 "Marcel": 60,
            #                 "René": 192,
            #                 "Paul": 178,
            #                 "Jacques": 29,
            #             },
            #             {
            #                 "Raoul": 22,
            #                 "Josiane": 114,
            #                 "Marcel": 15,
            #                 "René": 120,
            #                 "Paul": 29,
            #                 "Jacques": 132,
            #             },
            #             {
            #                 "Raoul": 101,
            #                 "Josiane": 80,
            #                 "Marcel": 151,
            #                 "René": 70,
            #                 "Paul": 131,
            #                 "Jacques": 106,
            #             },
            #             {
            #                 "Raoul": 162,
            #                 "Josiane": 27,
            #                 "Marcel": 31,
            #                 "René": 154,
            #                 "Paul": 160,
            #                 "Jacques": 82,
            #             },
            #             {
            #                 "Raoul": 123,
            #                 "Josiane": 92,
            #                 "Marcel": 18,
            #                 "René": 129,
            #                 "Paul": 11,
            #                 "Jacques": 15,
            #             },
            #         ]
            #
            #         nivo.Stream(
            #             data=data_area,
            #             keys=["Raoul", "Josiane", "Marcel", "René", "Paul", "Jacques"],
            #             margin={"top": 50, "right": 110, "bottom": 50, "left": 60},
            #             axisTop={"null"},
            #             axisBottom={
            #                 "orient": "bottom",
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "",
            #                 "legendOffset": 36,
            #             },
            #             axisLeft={
            #                 "orient": "left",
            #                 "tickSize": 5,
            #                 "tickPadding": 5,
            #                 "tickRotation": 0,
            #                 "legend": "",
            #                 "legendOffset": -40,
            #             },
            #             enableGridX={"true"},
            #             enableGridY={"false"},
            #             offsetType="silhouette",
            #             colors={"scheme": "nivo"},
            #             fillOpacity={0.85},
            #             borderColor={"theme": "background"},
            #             defs=[
            #                 {
            #                     "id": "dots",
            #                     "type": "patternDots",
            #                     "background": "inherit",
            #                     "color": "#2c998f",
            #                     "size": 4,
            #                     "padding": 2,
            #                     "stagger": "true",
            #                 },
            #                 {
            #                     "id": "squares",
            #                     "type": "patternSquares",
            #                     "background": "inherit",
            #                     "color": "#e4c912",
            #                     "size": 6,
            #                     "padding": 2,
            #                     "stagger": "true",
            #                 },
            #             ],
            #             fill=[
            #                 {"match": {"id": "Paul"}, "id": "dots"},
            #                 {"match": {"id": "Marcel"}, "id": "squares"},
            #             ],
            #             dotSize={8},
            #             dotColor={"from": "color"},
            #             dotBorderWidth={2},
            #             dotBorderColor={
            #                 "from": "color",
            #                 "modifiers": [["darker", 0.7]],
            #             },
            #             legends=[
            #                 {
            #                     "anchor": "bottom-right",
            #                     "direction": "column",
            #                     "translateX": 100,
            #                     "itemWidth": 80,
            #                     "itemHeight": 20,
            #                     "itemTextColor": "#999999",
            #                     "symbolSize": 12,
            #                     "symbolShape": "circle",
            #                     "effects": [
            #                         {
            #                             "on": "hover",
            #                             "style": {"itemTextColor": "#000000"},
            #                         }
            #                     ],
            #                 }
            #             ],
            #             theme={
            #                 "background": "#00cccc",
            #                 "textColor": "white",
            #                 "tooltip": {
            #                     "container": {
            #                         "background": "#FFFFFF",
            #                         "color": "#31333F",
            #                     }
            #                 },
            #             },
            #         )

            with mui.Card(
                key="漏斗图",
                sx={
                    "color": "black",
                    "bgcolor": "#ffffff",
                    "borderRadius": 0,
                    "display": "flex",
                    "flexDirection": "column",
                },
            ):
                mui.CardHeader(title="漏斗图", className="draggable")
                with mui.CardContent(sx={"flex": 2, "minHeight": 0}):

                    data_loudou = [
                        {"id": "step_sent", "value": 83250, "label": "Sent"},
                        {"id": "step_viewed", "value": 62823, "label": "Viewed"},
                        {"id": "step_clicked", "value": 50860, "label": "Clicked"},
                        {
                            "id": "step_add_to_card",
                            "value": 42885,
                            "label": "Add To Card",
                        },
                        {"id": "step_purchased", "value": 25865, "label": "Purchased"},
                    ]
                    nivo.Funnel(
                        data=data_loudou,
                        margin={"top": 0, "right": 20, "bottom": 20, "left": 20},
                        valueFormat=">-.4s",
                        colors={"scheme": "spectral"},
                        borderWidth={30},
                        labelColor={"from": "color", "modifiers": [["darker", 3]]},
                        theme={
                            "background": "transparent",
                            "textColor": "white",
                            "tooltip": {
                                "container": {
                                    "background": "#FFFFFF",
                                    "color": "#31333F",
                                }
                            },
                        },
                    )

