import streamlit as st
from tools.mysqlConnect import mysqlObject
from tools.configReader import configReader
from tools.echartsPlot import BarLinePlot
from tools.dateTool import dataframeDateAssign
from streamlit_echarts import st_echarts
from datetime import datetime, timedelta
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pandas as pd
import re

daMysqlConfi = configReader("./config/config.ini").readDBInfo("mysql-analysis-offline")
daMysql = mysqlObject(*daMysqlConfi)


@st.experimental_memo
def loadKeyWordLog(sd, ed, search_count=None, nst=None, nst_type='小于'):
    Sql = f"""
    select * from searchkeyTarget
    where pdate >= '{sd}' 
    and pdate <= '{ed}' 
    """
    if search_count:
        Sql += f" and search_count >= '{search_count}'"
    if nst:
        if nst_type == '小于':
            Sql += f" and nst <= {nst}"
        else:
            Sql += f" and nst >= {nst}"
    return daMysql.queryData(Sql)


@st.experimental_memo
def loadExactKey(sd, ed, keyword):
    Sql = f"""
    select * from searchkeyTarget
    where pdate >= '{sd}' 
    and pdate <= '{ed}'  
    and keyword = BINARY '{keyword}'
    """
    return daMysql.queryData(Sql)


@st.experimental_memo
def loadKeyWordTarget(sd, ed):
    Sql = f"""
    select * from searchkeyALLTarget
    where pdate >= '{sd}' 
    and pdate <= '{ed}'
    """
    return daMysql.queryData(Sql)


def getEveryDay(begin_date, end_date):
    # 前闭后闭
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


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
def defaultKeywords():
    Sql = """
    select text from notebook
    where record_subject = '默认查询搜索词'
    """
    return daMysql.queryData(Sql)['text'].tolist()[0]


def main():
    st.title("搜索")
    colors = st.session_state["colorTheme"]
    st.header("指标")
    c1, c2 = st.columns(2)
    sd = str(c1.date_input("Start Date", value=datetime.today() + timedelta(days=-14)))
    ed = str(c2.date_input("End Date", value=datetime.today() + timedelta(days=-1)))
    if ed < sd:
        ed, sd = sd, ed
    data1 = loadKeyWordTarget(sd, ed)
    data1 = pd.merge(pd.DataFrame({'pdate': getEveryDay(sd, ed)}), data1, on='pdate', how='left').fillna(0)
    data1 = dataframeDateAssign(data1)
    st_echarts(BarLinePlot(data1, xCol='pdate', yLineCols=['nst'], Title="NsT指标", showAvgLine=True, colors=colors))
    st.write('---')

    st.subheader("搜索词NsT指标趋势")
    defaultKey = defaultKeywords()
    st.info("输入搜索词(多个搜索词用逗号隔开),    "
            "修改默认展示搜索词----> 记事本模块修改id=9的事件")
    search_word = st.text_input("", value=defaultKey, label_visibility='hidden').strip()
    search_words = re.split(r'[，,]', search_word)
    i = 0
    cs = st.columns(2)
    for j, words in enumerate(search_words):
        words = words.strip()
        if (j % 2 == 0) and (j > 0):
            cs = st.columns(2)
        with cs[j % 2]:
            data_ = loadExactKey(sd, ed, words)
            st_echarts(BarLinePlot(data_, xCol='pdate', yLineCols=['nst'], yBarCols=['search_count'], Title=f"NsT-{words}", colors=colors), key=i)
            i += 1
    # data4 = loadExactKey(sd, ed, search_word)
    # st.write(loadExactKey(sd, ed, '土豆'))

    st.write('---')

    st.subheader("关键词指标数据下载（选择日期前推14天）")
    c3, c4, c5, c6, c7 = st.columns(5)
    select_date = c3.selectbox("选择日期", options=data1.pdate.unique().tolist())
    search_count_limit = c4.selectbox('搜索次数大于等于', options=[None, 3, 4, 5, 6, 7, 8, 9, 10, 11], index=3)
    nst_limit = c6.selectbox('Nst限制', options=[None, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    nst_type = c5.selectbox('Nst区间', options=['小于', '大于'])
    data3 = loadKeyWordLog(select_date, select_date, search_count_limit, nst_limit, nst_type).iloc[:, 2:]
    xls3 = to_excel(data3)
    with c7:
        if_show = st.checkbox("显示数据")
        st.download_button(
            label='📥 下载搜索词NsT数据',
            data=xls3,
            file_name=f'{select_date}_搜索词NsT数据.xlsx')
    if if_show:
        st.write(data3)
    st.write('---')


