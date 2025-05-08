# ✅ streamlit_app.py

import streamlit as st
import subprocess
import time
import webbrowser

st.set_page_config(page_title="日経平均 終値予測", page_icon="📈")
st.title("📈 日経平均 終値予測アプリ")

st.markdown("""
このアプリは、日経平均先物・CME先物・NYダウ・ドル円レートの変化率から、
**当日の日経平均終値を予測**するツールです。
""")

if st.button("予測を実行"):
    # 実行対象のスクリプトを呼び出し（ここでは仮に nikkei_web.py を使うとする）
    try:
        with st.spinner("予測中...少々お待ちください"):
            result = subprocess.run([
                "python", "nikkei_web.py"
            ], capture_output=True, text=True)

        st.success("予測完了！")
        st.code(result.stdout)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
