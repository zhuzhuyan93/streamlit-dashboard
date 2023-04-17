import numpy as np
import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from tools.publicComponent import *
from datetime import datetime, timedelta
from tools.mysqlConnect import mysqlObject
from tools.configReader import configReader
from tools.echartsPlot import BarLinePlot
from tools.dateTool import dataframeDateAssign
from streamlit_card import card
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

daMysqlConfi = configReader("./config/config.ini").readDBInfo("mysql-analysis-offline")
daMysql = mysqlObject(*daMysqlConfi)

group_map = {"ALL": "未分组", "A": "实验组", "B": "对照组"}

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

@st.experimental_memo
def loadTargetData(startDate, endDate, sn=None, en=None):
    Sql = f"""
        select *
        from guess_target_data
        where pdate >= '{startDate}' and pdate <= '{endDate}'
        """
    if sn:
        Sql += f"and pageindex >= {sn} "
    if en:
        Sql += f"and pageindex <= {en} "
    Data = daMysql.queryData(Sql)
    return Data


@st.experimental_memo
def loadTurnPage(startDate, endDate):
    Data = daMysql.queryData(
        f"""
    select *
    from guess_turn_page
    where pdate >= '{startDate}' and pdate <= '{endDate}'
    """
    )
    return Data


def main():
    st.title("猜你喜欢")
    colors = st.session_state["colorTheme"]

    st.subheader("指标")
    colors = st.session_state["colorTheme"]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        sd, ed = [
            str(i)
            for i in st.date_input(
                "Date Range",
                value=[
                    datetime.today() + timedelta(days=-14),
                    datetime.today() + timedelta(days=-1),
                ],
                key=4324,
            )
        ]

    with c4:
        for _ in range(2):
            st.write("\n")
        show_type = "PV"
        if st.checkbox("Display As UV"):
            show_type = "UV"

    with c2:
        sn = st.selectbox("开始页码", [None] + list(range(1, 12)))
    with c3:
        en = st.selectbox("结束页码", [None] + list(range(1, 12)), index=5)

    if isinstance(sn, int) and isinstance(en, int) and sn > en:
        st.error("开始页码大于结束页码时，结束页码只能选择None。")
    else:
        if show_type == "PV":
            # 添加分组的总和数据
            data = (
                loadTargetData(sd, ed, sn, en)
                .groupby(["pdate", "shunt_name"])[["exp_pv", "clk_pv"]]
                .sum()
                .reset_index()
                .assign(
                    shunt_name=lambda x: x["shunt_name"].map(group_map),
                )
            )
            data_ = (
                data.loc[lambda x: x["pdate"] > "2022-11-23"]
                .groupby(["pdate"])[["exp_pv", "clk_pv"]]
                .sum()
                .reset_index()
                .assign(shunt_name="未分组")
            )
            dataPlot = pd.concat([data, data_], axis=0)

            dataPlot1 = (
                dataPlot.assign(exp_rate=lambda x: x["clk_pv"] / x["exp_pv"])
                .pivot(index="pdate", columns="shunt_name", values="exp_rate")
                .fillna(0)
                .reset_index()
            )
            dataPlot2 = (
                dataPlot.assign(exp_rate=lambda x: x["clk_pv"] / x["exp_pv"])
                .pivot(index="pdate", columns="shunt_name", values=["exp_pv", "clk_pv"])
                .fillna(0)
            )
            dataPlot2.columns = [
                "-".join(i).replace("exp_pv", "曝光量").replace("clk_pv", "点击量")
                for i in dataPlot2.columns
            ]
            dataPlot2 = dataPlot2.reset_index()
            dataPlot1 = dataframeDateAssign(dataPlot1)
            dataPlot2 = dataframeDateAssign(dataPlot2)
            c1, c2 = st.columns((9, 1))
            with c1:
                st_echarts(
                    BarLinePlot(
                        dataPlot1,
                        xCol="pdate",
                        yLineCols=["实验组", "对照组", "未分组"],
                        yLineFormat=True,
                        Title="曝光点击率-PV",
                        showAvgLine=True,
                        colors=colors,
                    )
                )
            with c2:
                st.metric(
                    label="实验组均值",
                    value=f"{np.round(dataPlot1['实验组'].mean() * 100, 2)}%",
                    delta=f"{np.round(((dataPlot1['实验组'].mean() - dataPlot1['对照组'].mean()) / dataPlot1['对照组'].mean()) * 100, 2)}%",
                    # delta_color="off",
                )
            c1, c2 = st.columns((9, 1))
            with c1:
                st_echarts(
                    BarLinePlot(
                        dataPlot2,
                        xCol="pdate",
                        yBarCols=["点击量-实验组", "点击量-对照组", "点击量-未分组"],
                        yLineCols=["曝光量-实验组", "曝光量-对照组", "曝光量-未分组"],
                        # yLineFormat=True,
                        Title="曝光点击量-PV",
                        showAvgLine=True,
                        colors=colors,
                    )
                )
            with c2:
                st.metric(
                    label="实验组曝光量均值",
                    value=f"{int(dataPlot2['曝光量-实验组'].mean() )}",
                    delta=f"{np.round(((dataPlot2['曝光量-实验组'].mean() - dataPlot2['曝光量-对照组'].mean()) / dataPlot2['曝光量-对照组'].mean()) * 100, 2)}%",
                    # delta_color="off",
                )
        else:
            st.warning("曝光点击率-UV 无法显示页码范围，只显示单页数据（结束页码）。")
            if en:
                data = (
                    loadTargetData(sd, ed, en, en)
                    .assign(
                        shunt_name=lambda x: x["shunt_name"].map(group_map),
                        clk_rate=lambda x: x["clk_uv"] / x["exp_uv"],
                    )
                    .pivot(index="pdate", columns="shunt_name", values="clk_rate")
                    .reset_index()
                )
                data = dataframeDateAssign(data)
                st_echarts(
                    BarLinePlot(
                        data,
                        xCol="pdate",
                        yLineCols=["实验组", "对照组"],
                        yLineFormat=True,
                        Title=f"曝光点击率-UV-第{en}页",
                        colors=colors,
                    )
                )
            else:
                st.info("选择具体的结束页码。")

    st.write("---")
    st.subheader("拓展")
    c1, c2 = st.columns(2)
    data2 = loadTurnPage(sd, ed)
    data2_1 = data2.groupby(["pageindex"], as_index=False)["request_num"].sum()
    data2_1 = data2_1.rename(columns={"pageindex": "单次浏览最大翻页", "request_num": "浏览次数"})
    data2_1 = data2_1.assign(
        浏览次数占比=lambda x: x["浏览次数"] / x["浏览次数"].sum(),
        浏览次数累计占比=lambda x: np.cumsum(x["浏览次数占比"]),
    )
    data2_2 = (
        data2.assign(req_sum=lambda x: x["pageindex"] * x["request_num"])
        .groupby("pdate")[["request_num", "req_sum"]]
        .sum()
        .assign(平均最大翻页=lambda x: x["req_sum"] / x["request_num"])
        .reset_index()
    )

    # st.write(data2_2)
    with c1:
        st_echarts(
            BarLinePlot(
                data2_1,
                xCol="单次浏览最大翻页",
                yLineCols=["浏览次数累计占比"],
                colors=colors,
                Title="单次浏览最大翻页分布",
            )
        )
        xls1 = to_excel(data2_1)
        st.download_button(
            label='📥 下载Excel文件',
            data=xls1,
            file_name='单次浏览最大翻页分布.xlsx')
    with c2:
        st_echarts(
            BarLinePlot(
                data2_2,
                xCol="pdate",
                yLineCols=["平均最大翻页"],
                colors=colors,
                Title="平均最大翻页",
            )
        )
        xls2 = to_excel(data2_2)
        st.download_button(
            label='📥 下载Excel文件',
            data=xls2,
            file_name='平均最大翻页.xlsx')
    # st.write(data2)
