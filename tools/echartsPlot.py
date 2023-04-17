import streamlit as st
import numpy as np


def BarLinePlot(
    df,
    xCol=None,
    yBarCols=None,
    yLineCols=None,
    Title="",
    plotType="bar",
    yBarFormat=False,
    yLineFormat=False,
    colors=st.session_state.get("colorTheme"),
    showAvgLine=False,
):
    """
    :param showAvgLine: 是否显示均值线
    :param colors:
    :param df: pandasDataframe
    :param xCol:X
    :param yBarCols:BarY
    :param yLineCols:LineY
    :param Title:PlotTitle
    :param plotType: 只有yBarCols和yLineCols都为空时起作用
    :param yBarFormat: 是否转化为百分数
    :param yLineFormat: 是否转化为百分数
    :return: option
    Bar or Line or Multi support
    """
    if not xCol:
        xData = list(df.index)
    else:
        if isinstance(xCol, list):
            xCol = xCol[0]
        xData = df[xCol].tolist()

    if yBarFormat:
        bft = "%"
    else:
        bft = ""

    if yLineFormat:
        lft = "%"
    else:
        lft = ""

    if (yBarCols is None) & (yLineCols is None):
        if plotType == "bar":
            yBarCols = list(df.columns)
        else:
            yLineCols = list(df.columns)

    if (yBarCols is not None) & (yLineCols is None):
        yAxis = [
            {
                "type": "value",
                "name": "BarAxis",
                "axisLabel": {"formatter": "{value}" + f"{bft}"},
            }
        ]
        if yBarFormat:
            yBarData = [np.round(df[Col] * 100, 3).tolist() for Col in yBarCols]
        else:
            yBarData = [np.round(df[Col], 3).tolist() for Col in yBarCols]
        yLineData = []
        yLineCols = []
        yAxisBarIndex = 0
        yAxisLineIndex = 1
    elif (yBarCols is not None) & (yLineCols is not None):
        yAxis = [
            {
                "type": "value",
                "name": "BarAxis",
                "axisLabel": {"formatter": "{value}" + f"{bft}"},
            },
            {
                "type": "value",
                "name": "LineAxis",
                "axisLabel": {"formatter": "{value}" + f"{lft}"},
            },
        ]
        if yBarFormat:
            yBarData = [np.round(df[Col] * 100, 3).tolist() for Col in yBarCols]
        else:
            yBarData = [np.round(df[Col], 3).tolist() for Col in yBarCols]

        if yLineFormat:
            yLineData = [np.round(df[Col] * 100, 3).tolist() for Col in yLineCols]
        else:
            yLineData = [np.round(df[Col], 3).tolist() for Col in yLineCols]

        yAxisBarIndex = 0
        yAxisLineIndex = 1
    else:
        yAxis = [
            {
                "type": "value",
                "name": "LineAxis",
                "axisLabel": {"formatter": "{value}" + f"{lft}"},
            }
        ]
        if yLineFormat:
            yLineData = [np.round(df[Col] * 100, 2).tolist() for Col in yLineCols]
        else:
            yLineData = [np.round(df[Col], 2).tolist() for Col in yLineCols]

        yBarData = []
        yBarCols = []
        yAxisLineIndex = 0
        yAxisBarIndex = 1

    markline = False
    if showAvgLine:
        markline = {
            "data": [{"type": "average", "name": "平均值", "silent": True}],
            "label": {"position": "end"},
            "symbol": "none",
        }

    option = {
        "title": {"text": Title},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "confine": True,
        },
        "grid": {
            "show": False,
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True,
        },
        "color": colors,
        "legend": {
            "orient": "horizontal",
            "x": "20%",
            "y": "8%",
            "width": "60%",
            "type": "scroll",
        },
        "xAxis": [
            {
                "type": "category",
                "data": xData,
                "axisTick": {"alignWithLabel": "true"},
                # "axisLabel": {"interval": 0},
            }
        ],
        "yAxis": yAxis,
        "series": [
            {
                "name": Label,
                "type": "bar",
                "barWidth": "25%",
                "yAxisIndex": yAxisBarIndex,
                "data": Data,
                # "showBackground": True,
                # "backgroundStyle": {"color": "rgba(180, 180, 180, 0.1)"},
                "itemStyle": {
                    "emphasis": {"barBorderRadius": [10, 10]},
                    "normal": {"barBorderRadius": [6, 6, 0, 0]},
                },
                # "color": ,
            }
            for Data, Label in zip(yBarData, yBarCols)
        ]
        + [
            {
                "name": Label,
                "type": "line",
                "yAxisIndex": yAxisLineIndex,
                "data": Data,
                "smooth": "true",
                "markLine": markline,
                "lineStyle": {"color": colors[i]},
                "itemStyle": {
                    "color": colors[i]
                }
            }
            for i, Data, Label in zip(range(len(yLineData)), yLineData, yLineCols)
        ],
    }
    return option
