import streamlit as st
import plotly.graph_objects as go
import requests
import json
import time

# 設定ファイルの読み込み
with open('nodes.json') as config_file:
    config = json.load(config_file)

nodes = config["nodes"]

def get_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return None

def create_indicator_chart(title, value, max_value=100):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0, max_value]}}
    ))

st.title('System and GPU Information')

# サイドバーでノード情報を表示
st.sidebar.markdown("#### 研究エリア")
st.sidebar.markdown("""
<table>
    <tr>
        <tr colspan='2' align='center'>先生の部屋</td>
    </tr>
    <tr>
        <td>踏み台</td>
        <td>Node 2 <br> (192.168.0.24)</td>
    </tr>
    <tr>
        <td>Node 1 <br> (192.168.0.18)</td>
        <td>Node 3 <br> (192.168.0.32)</td>
    </tr>
    <tr>
        <td>Node 4 <br> (192.168.0.34)</td>
        <td>Node 5 <br> (192.168.0.36)</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.sidebar.markdown("#### クラウド基盤室")
st.sidebar.markdown("""
<table>
    <tr><td>Node 6 <br> (192.168.2.2)</td></tr>
    <tr><td>Node 7 <br> (192.168.2.3)</td></tr>
</table>
""", unsafe_allow_html=True)

st.sidebar.write("")

selected_node = st.sidebar.selectbox("Select a node", list(nodes.keys()))
url = nodes[selected_node]
json_data = get_json_data(url)
st.header(f'System Info: {json_data["System Info"]["IP Address"]}')
# システム情報とGPUステータス用のプレースホルダー
sys_info_placeholder = st.empty()
gpu_status_placeholder = st.empty()

def update_display():
    url = nodes[selected_node]
    json_data = get_json_data(url)
    
    if json_data:
        with sys_info_placeholder.container():
            # st.header(f'System Info: {json_data["System Info"]["IP Address"]}')
            login_users = ', '.join(json_data["System Info"]["Login Users"])
            st.subheader(f"Login Users: {login_users}")

            col1, col2 = st.columns(2)
            with col1:
                cpu_usage = float(json_data['System Info']['CPU Usage'].strip('%'))
                fig_cpu = create_indicator_chart("CPU 使用率", cpu_usage)
                fig_cpu.update_layout(width=250, height=250, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_cpu, use_container_width=True)

            with col2:
                memory_usage = float(json_data['System Info']['Memory Usage'].strip('%'))
                fig_memory = create_indicator_chart("Memory 使用率", memory_usage)
                fig_memory.update_layout(width=250, height=250, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_memory, use_container_width=True)

        with gpu_status_placeholder.container():
            st.header('GPU Status')
            for gpu in json_data['GPU Status']:
                st.subheader(f"GPU Index: {gpu['GPU Index']} ({gpu['GPU Name']})")
                col1, col2 = st.columns(2)
                with col1:
                    gpu_utilization = float(gpu['GPU Utilization'].strip(' %'))
                    fig_gpu_util = create_indicator_chart("GPU 使用率", gpu_utilization)
                    fig_gpu_util.update_layout(width=250, height=250, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_gpu_util, use_container_width=True)

                with col2:
                    memory_utilization = float(gpu['Memory Utilization'].strip(' %'))
                    fig_memory_util = create_indicator_chart("Memory 使用率", memory_utilization)
                    fig_memory_util.update_layout(width=250, height=250, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_memory_util, use_container_width=True)

# 初期表示
update_display()

# 定期的な更新
while True:
    time.sleep(1)
    update_display()
