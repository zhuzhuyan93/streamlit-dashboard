import streamlit as st
from tools.mysqlConnect import mysqlObject
from tools.configReader import configReader
from tools.echartsPlot import BarLinePlot
from tools.dateTool import dataframeDateAssign
from streamlit_echarts import st_echarts
from datetime import datetime, timedelta

daMysqlConfi = configReader("./config/config.ini").readDBInfo("mysql-analysis-offline")
daMysql = mysqlObject(*daMysqlConfi)


@st.experimental_memo
def loadShopHotClick(sd, ed):
    return daMysql.queryData(
        f"""
        select * from shop_hot_click_uv_pv
        where pdate >= '{sd}' and pdate <= '{ed}' 
        """
    )


@st.experimental_memo
def loadEventModule(sd, ed):
    return daMysql.queryData(
        f"""
        select * from eventCodeDistribution
        where pdate >= '{sd}' and pdate <= '{ed}'
        """
    )


def main():
    st.title("数据异常监控")
    colors = st.session_state["colorTheme"]
    c1, c2 = st.columns(2)
    with c1:
        sd, ed = [
            str(i)
            for i in st.date_input(
                "Date Range",
                value=[
                    datetime.today() + timedelta(days=-28),
                    datetime.today() + timedelta(days=-1),
                ],
                key=4324,
            )
        ]

    with c2:
        for _ in range(2):
            st.write("\n")
        show_type = "PV"
        if st.checkbox("Display As UV"):
            show_type = "UV"

    # 总览数据

    st.subheader("🍅基础数据统计")
    event_map = {
        "menu_click": "菜谱点击事件",
        "menu_view": "菜谱浏览事件",
        "menu_start_cooking": "菜谱开始烹饪事件",
        "menu_recooking": "菜谱补炊事件",
        "menu_finish_cooking": "菜谱完成烹饪事件",
        "menu_add_to_plan": "菜谱添加计划事件",
        "menu_collect": "菜谱收藏事件",
    }
    dataAll = (
        loadEventModule(sd, ed)
        .drop(columns=["ID"])
        .assign(event_code=lambda x: x["event_code"].map(event_map))
    )
    dataAll = (
        dataAll.pivot(
            index=["pdate", "event_code"], columns=["os"], values=show_type.lower()
        )
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    i = 0
    cs = st.columns(2)
    for value in event_map.values():
        if (i % 2 == 0) and (i > 0):
            cs = st.columns(2)
        df_plot = dataAll.loc[lambda x: x["event_code"] == value]
        df_plot = dataframeDateAssign(df_plot)
        yLineCols = ["Android", "iOS", "ChiereOne"]
        if value in ["菜谱开始烹饪事件", "菜谱补炊事件", "菜谱完成烹饪事件"]:
            yLineCols = ["ChiereOne"]
        if value in ["菜谱收藏事件"]:
            yLineCols = ["Android", "iOS"]
        with cs[i % 2]:
            st_echarts(
                BarLinePlot(
                    df_plot,
                    xCol="pdate",
                    yLineCols=yLineCols,
                    colors=colors,
                    Title=value,
                    showAvgLine=True,
                ),
                key=i,
            )
        i += 1

    st.subheader("🍑场景维度")
    dataPlot = (
        loadShopHotClick(sd, ed)
        .drop(columns=["ID"])
        .groupby("pdate", as_index=False)
        .sum()
        .rename(columns={"clk_uv": "点击UV", "clk_pv": "点击PV"})
    )
    dataPlot = dataframeDateAssign(dataPlot)
    st_echarts(
        BarLinePlot(
            dataPlot,
            xCol="pdate",
            yLineCols=["点击UV", "点击PV"],
            colors=colors,
            Title="商城爆款推荐点击UV&PV",
            showAvgLine=True,
        )
    )
