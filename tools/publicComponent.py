import streamlit as st


def Button():
    with st.sidebar:
        # c1, c2, c3 = st.columns((1, 1, 2))
        # with c1:
        if st.button("刷新"):
            st.experimental_memo.clear()
        # with c3:
        colorTheme = st.selectbox(
            " ",
            [
                "主题1",
                "主题12",
            ],
            index=1,
            label_visibility="collapsed",
        )
        colorsDict = {
            "主题1": [
                "#9775fa",
                "#f06595",
                "#22b8cf",
                "#ff922b",
                "#fcc419",
                "#3bc9db",
                "#4dabf7",
                "#ced4da",
                "#94d82d",
                "#0078d4",
                "#107c10",
                "#5c2d91",
                "#b4009e",
                "#32145a",
                "#b4009e",
                "#5f27cd",
                "#f368e0",
            ],
            "主题12": ["#0780cf", "#765005", "#fa6d1d", "#0e2c82", "#b6b51f"],
        }
        st.session_state["colorTheme"] = colorsDict.get(colorTheme)
