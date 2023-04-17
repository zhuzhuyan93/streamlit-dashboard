import streamlit as st
import streamlit_authenticator as stauth
from streamlit_lottie import st_lottie
import json
from tools.assignCss import local_css
from tools.publicComponent import *
from contents import (
    page1_rec_for_u,
    page2_home_sub,
    page3_1_hot_rec,
    page3_2_shop_all,
    page0_data_consor,
    page4_search
)


# 个性化组件
def main_page():
    st.set_page_config(layout="wide", page_title="Homepage")
    local_css("./config/streamlitPageSet.css")
    with open(
        "./static/lottie/137680-meditating-rabbit.json", "r", encoding="utf-8"
    ) as f:
        content2 = json.load(f)

    Button()
    # 页面控制
    page_level1 = ["数据异常监控", '搜索', "猜你喜欢", "食万首页小专题", "商城"]  # 一级页面
    page_level2 = {"商城": ["爆款推荐", "整体模块"]}  # 二级页面
    page = st.sidebar.selectbox(
        "一级页面",
        page_level1,
        index=0,
    )
    if page in page_level2:
        page = st.sidebar.selectbox(
            "二级页面",
            page_level2.get(page),
            index=0,
        )

    # 页面设置
    page_level_dict = {
        "数据异常监控": page0_data_consor,
        "猜你喜欢": page1_rec_for_u,
        "食万首页小专题": page2_home_sub,
        "爆款推荐": page3_1_hot_rec,
        "整体模块": page3_2_shop_all,
        '搜索': page4_search
    }
    page_level_dict.get(page).main()
    with st.sidebar:
        for _ in range(10):
            st.write("\n")
        st_lottie(content2, key="show")


if __name__ == "__main__":
    main_page()
