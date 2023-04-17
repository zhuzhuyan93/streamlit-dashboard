import streamlit as st
from streamlit_echarts import st_echarts
from dataProcess.dbConnect import mysqlObject
import pandas as pd
import tools
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb


productMysql = mysqlObject(environment="offline")
plot = tools.Plot()
dateTool = tools.Date()


def page():
    st.title("商城整体模块")

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('ANSI')
    
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
    def load_tag_data():
        data_tag = productMysql.queryData(
            """
        select * from shop_food_standard_tag
        """
        )
        tag_col = ["cuisine", "taste", "dishes", "people", "scenario"]
        tagData = {}
        for tag in tag_col:
            vcDf = (
                pd.value_counts(
                    data_tag[[tag]]
                    .loc[lambda x: x[tag] != ""]
                    .assign(tag=lambda x: x[tag].str.split("|"))
                    .explode("tag")["tag"]
                )
                .to_frame()
                .reset_index()
            )
            tagData[tag] = vcDf

        return tagData

    @st.experimental_memo
    def load_source_data():
        data_source = productMysql.queryData(
            """
        select * from shop_click_add_source
        """
        )
        return data_source

    @st.experimental_memo
    def load_food_add_clk_info():
        data_info = productMysql.queryData(
            """
        select *
        from shop_clk_add_food_num
        where pdate >= date_sub(current_date, interval 30 day)
        """
        )
        return data_info

    @st.experimental_memo
    def load_order_data():
        OrderData = productMysql.queryData(
            """
            select *
            from shop_order_sale_status_info
            where pdate >= date_sub(current_date, interval 30 day)
        """
        )
        OrderData = (
            OrderData.pivot(
                index="pdate",
                columns=["order_status"],
                values=["goods_num", "order_num", "avg_goods_num"],
            )
            .fillna(0)
            .sort_index()
        )
        OrderData.columns = [
            (Col[1] + "_" + Col[0])
            .replace("avg_goods_num", "单均商品数")
            .replace("goods_num", "商品数量")
            .replace("order_num", "订单数量")
            for Col in OrderData.columns
        ]
        return OrderData

    @st.experimental_memo
    def load_order_all_data():
        OrderAllData = productMysql.queryData(
            """
        select * from shop_order_sale_all_info
        where pdate >= date_sub(current_date, interval 45 day)
        """
        )
        return OrderAllData

    @st.experimental_memo
    def load_user_activate_data():
        userData = productMysql.queryData(
            """
            select * from shop_order_user_activate_info
            """
        )
        return userData

    # 整体净菜标签分布

    st.subheader("整体净菜标签分布")
    tagData = load_tag_data()
    cols = st.columns(len(tagData))
    i = 0
    for key, value, col in zip(tagData.keys(), tagData.values(), cols):
        key = {
            "cuisine": "菜系",
            "taste": "口味",
            "dishes": "菜式",
            "people": "人群",
            "scenario": "场景",
        }.get(key)
        with col:
            st_echarts(
                tools.Plot().EchartsPiePlot(
                    value, nameCol="index", valueCol="tag", Title=key
                ),
                key=i,
            )
            i += 1

    # 商城点击加购来源分布
    source_data = load_source_data()
    st.subheader("商城点击加购来源分布")
    col1, col2 = st.columns(2)
    sd = col1.selectbox(
        "开始日期", options=sorted(source_data.pdate.unique(), reverse=True)
    )
    ed = col2.selectbox(
        "结束日期", options=sorted(source_data.pdate.unique(), reverse=True)
    )
    if ed < sd:
        ed, sd = sd, ed
    source_data_plot = (
        dateTool.PandasFilterDate(source_data, start_date=sd, end_date=ed)
        .groupby(["event", "page", "lib", "source"])[["num"]]
        .sum()
        .reset_index()
        .rename(columns={"num": "Number"})
    )
    col1, col2, col3 = st.columns(3)

    source_data_plot1 = (
        source_data_plot.loc[lambda x: x["event"] == "商品添加购物车"]
        .groupby("page")
        .sum()
        .reset_index()
    )
    source_data_plot2 = (
        source_data_plot.loc[lambda x: x["event"] == "商品详情页浏览"]
        .groupby("lib")
        .sum()
        .reset_index()
    )
    source_data_plot3 = (
        source_data_plot.loc[lambda x: x["event"] == "商品添加购物车"]
        .groupby("source")
        .sum()
        .reset_index()
    )

    with col1:
        st_echarts(
            tools.Plot().EchartsBarLinePlot(
                source_data_plot1,
                xCol=["page"],
                yBarCols=["Number"],
                Title="商品添加购物车-页面来源",
            )
        )

    with col2:
        st_echarts(
            tools.Plot().EchartsBarLinePlot(
                source_data_plot2,
                xCol=["lib"],
                yBarCols=["Number"],
                Title="商品详情页浏览(商品点击)-客户端来源",
            )
        )

    with col3:
        st_echarts(
            tools.Plot().EchartsBarLinePlot(
                source_data_plot3,
                xCol=["source"],
                yBarCols=["Number"],
                Title="商品添加购物车-客户端来源",
            )
        )

    # 商城点击加购菜谱粒度透视
    st.subheader("净菜商品点击加购明细(近30天)")
    st.markdown("**时间透视**")
    data_info = load_food_add_clk_info()
    col1, col2 = st.columns(2)
    sd = col1.selectbox("开始日期", options=sorted(data_info.pdate.unique(), reverse=True))
    ed = col2.selectbox("结束日期", options=sorted(data_info.pdate.unique(), reverse=True))
    if ed < sd:
        ed, sd = sd, ed



    data_info_plot = (
        tools.Date()
        .PandasFilterDate(data_info, start_date=sd, end_date=ed)
        .groupby("menu_name")
        .sum()
        .reset_index()
        .drop(columns="ID")
        .sort_values("add_num", ascending=False)
        .rename(
            columns={
                "add_num": "加购数",
                "add_user": "加购用户数",
                "clk_num": "点击数",
                "clk_user": "点击用户数",
            }
        )
    )
    showFoods = st.slider("显示加购Top", 5, len(data_info_plot), 10)
    st_echarts(
        plot.EchartsBarLinePlot(
            data_info_plot.head(showFoods), xCol="menu_name", yBarCols=["加购数", "加购用户数"], Title="净菜加购明细"
        )
    )
    st_echarts(
        plot.EchartsBarLinePlot(
            data_info_plot.head(showFoods), xCol="menu_name", yBarCols=["点击数", "点击用户数"], Title="净菜点击明细"
        )
    )

    st.markdown("**商品透视**")
    good_name = st.selectbox("选择商品", data_info.menu_name.unique())
    data_info_plot2 = (
        data_info.loc[lambda x: x["menu_name"] == good_name]
        .sort_values("pdate")
        .rename(
            columns={
                "add_num": "加购数",
                "add_user": "加购用户数",
                "clk_num": "点击数",
                "clk_user": "点击用户数",
            }
        )
    )
    col1, col2 = st.columns(2)
    with col1:
        st_echarts(
            plot.EchartsBarLinePlot(
                data_info_plot2,
                xCol="pdate",
                yBarCols=["加购数", "加购用户数"],
                Title="商品加购分布",
            )
        )

    with col2:
        st_echarts(
            plot.EchartsBarLinePlot(
                data_info_plot2,
                xCol="pdate",
                yBarCols=["点击数", "点击用户数"],
                Title="商品点击分布",
            )
        )

    st.subheader("净菜商品订单透视")
    orderData = load_order_data().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st_echarts(
            plot.EchartsBarLinePlot(
                orderData,
                xCol="pdate",
                yLineCols=[i for i in orderData.columns if i.endswith("订单数量")],
                Title="净菜订单状态统计",
            )
        )
    with col2:
        st_echarts(
            tools.Plot().EchartsBarLinePlot(
                orderData,
                xCol="pdate",
                yLineCols=[i for i in orderData.columns if i.endswith("商品数量")],
                Title="净菜商品状态统计",
            )
        )
    st_echarts(
        plot.EchartsBarLinePlot(
            orderData,
            xCol="pdate",
            yLineCols=[i for i in orderData.columns if i.endswith("单均商品数")],
            Title="净菜单均商品数统计",
        )
    )

    st.subheader("净菜订单明细")
    orderAllData = load_order_all_data()
    col1, col2, col3 = st.columns((2, 1, 1))
    orderStatus = col1.multiselect(
        "选择订单状态",
        set(
            list(orderAllData.order_status.unique())
            + ["待付款", "已付款", "待发货", "已发货", "已签收", "确认收货"]
        ),
        ["待付款", "已付款", "待发货", "已发货", "已签收", "确认收货"],
    )
    sd = col2.selectbox("开始日期", list(orderAllData.pdate.unique()), key=24)
    ed = col3.selectbox(
        "结束日期", sorted(list(orderAllData.pdate.unique()), reverse=True), key=25
    )
    if ed < sd:
        ed, sd = sd, ed
    orderAllDataPlot = (
        orderAllData.loc[
            lambda x: (x["order_status"].isin(orderStatus))
            & (x["pdate"] >= sd)
            & (x["pdate"] <= ed)
        ]
        .groupby(["pdate", "menu_name", "city", "province"])["sale_num"]
        .sum()
        .reset_index()
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**净菜TOP**")
        orderShow1 = (
            orderAllDataPlot.groupby("menu_name")["sale_num"]
            .sum()
            .reset_index()
            .sort_values(by="sale_num", ascending=False)
            .rename(columns={"menu_name": "净菜", "sale_num": "净菜数"})
        )
        orderShow1.index = range(1, len(orderShow1) + 1)
        # csv1 = convert_df(orderShow1) 
        # st.download_button(
        #     label="Download data as CSV",
        #     data=csv1,
        #     file_name='data.csv',
        #     mime='text/csv',
        # )
        xls1 = to_excel(orderShow1)
        st.download_button(
            label='📥 下载Excel文件',
            data=xls1 ,
            file_name= 'data.xlsx')
        st.dataframe(orderShow1, use_container_width=True)
    with col2:
        st.markdown("**城市TOP**")
        orderShow2 = (
            orderAllDataPlot.groupby("city")["sale_num"]
            .sum()
            .reset_index()
            .sort_values(by="sale_num", ascending=False)
            .rename(columns={"city": "城市", "sale_num": "净菜数"})
        )
        orderShow2.index = range(1, len(orderShow2) + 1)
        # csv2 = convert_df(orderShow2) 
        # st.download_button(
        #     label="Download data as CSV",
        #     data=csv2,
        #     file_name='data.csv',
        #     mime='text/csv',
        # )
        xls2 = to_excel(orderShow2)
        st.download_button(
            label='📥 下载Excel文件',
            data=xls2,
            file_name= 'data.xlsx')
        st.dataframe(orderShow2, use_container_width=True)
    with col3:
        st.markdown("**省份TOP**")
        orderShow3 = (
            orderAllDataPlot.groupby("province")["sale_num"]
            .sum()
            .reset_index()
            .sort_values(by="sale_num", ascending=False)
            .rename(columns={"province": "省份", "sale_num": "净菜数"})
        )
        orderShow3.index = range(1, len(orderShow3) + 1)
        # csv3 = convert_df(orderShow3) 
        # st.download_button(
        #     label="Download data as CSV",
        #     data=csv3,
        #     file_name='data.csv',
        #     mime='text/csv',
        # )
        xls3 = to_excel(orderShow3)
        st.download_button(
            label='📥 下载Excel文件',
            data=xls3,
            file_name= 'data.xlsx')
        st.dataframe(orderShow3, use_container_width=True)

    st.subheader("用户购买行为统计(近45天)")
    ##############

    @st.experimental_memo
    def load_shop_order_user_activate_info_all_target():
        Data = productMysql.queryData(
            """
            select * from shop_order_user_activate_info_all_target
            """
        )
        return Data

    liquidData = load_shop_order_user_activate_info_all_target()
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st_echarts(
                plot.EchartsLiquidPlot(
                    liquidData.iloc[i, 2], Title=liquidData.iloc[i, 1]
                ),
                key=i + 10,
            )

    @st.experimental_memo
    def load_shop_order_user_activate_info_all_agg():
        Data1 = productMysql.queryData(
            """
            select * from shop_order_user_activate_info_all_agg1
            """
        )
        Data2 = productMysql.queryData(
            """
            select * from shop_order_user_activate_info_all_agg2
            """
        )
        return Data1, Data2

    disAll = load_shop_order_user_activate_info_all_agg()
    titles = ["近45天订单数分布", "近45天订单活跃天数分布"]
    for i, col in enumerate(st.columns(2)):
        with col:
            st_echarts(
                plot.EchartsBarLinePlot(
                    disAll[i], xCol="index", yBarCols=["人数"], Title=titles[i]
                )
            )

    st.subheader("净菜商品购买用户RFM分析(近45天)")

    @st.experimental_memo
    def load_shop_order_user_activate_info_percentile():
        Data = productMysql.queryData(
            """
        select * from shop_order_user_activate_info_percentile
        """
        )
        return Data

    perData = load_shop_order_user_activate_info_percentile().set_index("per")
    df_r = pd.DataFrame(
        data=[
            (5, f"<={perData.loc['20%', 'r']}"),
            (4, f"{perData.loc['20%', 'r']} ~ {perData.loc['40%', 'r']}"),
            (3, f"{perData.loc['40%', 'r']} ~ {perData.loc['60%', 'r']}"),
            (2, f"{perData.loc['60%', 'r']} ~ {perData.loc['80%', 'r']}"),
            (1, f">{perData.loc['80%', 'r']}"),
        ],
        columns=["R评分", "范围"],
    )
    df_f = pd.DataFrame(
        data=[
            (5, f">5"),
            (4, f"3 ~ 5"),
            (3, f"2 ~ 3"),
            (2, f"1 ~ 2"),
            (1, f"<=1"),
        ],
        columns=["F评分", "范围"],
    )
    df_m = pd.DataFrame(
        data=[
            (1, f"<={perData.loc['20%', 'm']}"),
            (2, f"{perData.loc['20%', 'm']} ~ {perData.loc['40%', 'm']}"),
            (3, f"{perData.loc['40%', 'm']} ~ {perData.loc['60%', 'm']}"),
            (4, f"{perData.loc['60%', 'm']} ~ {perData.loc['80%', 'm']}"),
            (5, f">{perData.loc['80%', 'm']}"),
        ],
        columns=["M评分", "范围"],
    )
    st.markdown("**RFM参数阈值(分位数)**")
    for col, df in zip(st.columns(3), [df_r, df_f, df_m]):
        with col:
            st.table(df,)

    df_ceil = pd.DataFrame(
        data=[
            (1, 1, 1, "重要价值用户"),
            (1, 1, 0, "消费潜力用户"),
            (1, 0, 1, "频次深耕用户"),
            (1, 0, 0, "新用户"),
            (0, 1, 1, "高价值警惕流失用户"),
            (0, 1, 0, "一般高频用户"),
            (0, 0, 1, "高消费需挽回用户"),
            (0, 0, 0, "流失用户"),
        ],
        columns=["R是否大于均值", "F是否大于均值", "M是否大于均值", "用户分层"],
    )
    st.markdown("**用户业务分层**")
    st.table(df_ceil, )

    @st.experimental_memo
    def load_shop_order_user_activate_info_agg():
        Data = productMysql.queryData(
            """
        select * from shop_order_user_activate_info_agg
        """
        )
        return Data

    groupData = load_shop_order_user_activate_info_agg().rename(
        columns={
            "users": "人数",
            "user_perct": "人数占比",
            "cash": "消费金额",
            "cash_perct": "消费金额占比",
        }
    )
    st_echarts(
        plot.EchartsBarLinePlot(
            groupData,
            xCol="userGroup",
            yBarCols=["人数"],
            yLineCols=["人数占比"],
            yLineFormat=True,
            Title="分层用户人数分布",
        )
    )
    st_echarts(
        plot.EchartsBarLinePlot(
            groupData,
            xCol="userGroup",
            yBarCols=["消费金额"],
            yLineCols=["消费金额占比"],
            yLineFormat=True,
            Title="分层用户消费金额分布",
        )
    )

    # st.write(groupData)
    groupChoose = st.multiselect(
        "选择用户分群",
        [
            "重要价值用户",
            "一般高频用户",
            "高价值警惕流失用户",
            "消费潜力用户",
            "频次深耕用户",
            "新用户",
            "高消费需挽回用户",
            "流失用户",
        ],
        [
            "重要价值用户",
            "一般高频用户",
        ],
        key=100
    )
    if st.button("查询"):
        groups = "'" + "','".join(groupChoose)+ "'"
        showData = productMysql.queryData(f"""
        select *
        from aidata.shop_order_user_activate_info
        where userGroup in ({groups})
        """).iloc[:, 1:]
        st.write(showData)



