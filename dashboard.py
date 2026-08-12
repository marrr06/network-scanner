import streamlit
import sqlite3
import pandas


streamlit.set_page_config(
    page_title="Network Scanner Dashboard",
    page_icon="",
    layout="wide")
streamlit.title("Network Security Monitor")
streamlit.write("Monitor in real time devices connected to your network.")

def load_data():
    conn = sqlite3.connect("devices.db")
    df = pandas.read_sql_query("SELECT * FROM devices", conn)
    return df #returns table transformed in DataFrame data structure

df = load_data()
if not df.empty:
    col1, col2 = streamlit.columns(2)

    with col1:
        streamlit.subheader("Found Devices")
        display_df = df[['ip', 'mac', 'vendor', 'last_seen']].copy()
        streamlit.dataframe(display_df, use_container_width=True)

    with col2:
        streamlit.subheader("Network Traffic (in Bytes)")
        #only devices which have generated some kind of traffic will show
        traffic_df = df[df['bandwidth'] > 0][['ip', 'bandwidth']]
        
        if not traffic_df.empty:
            # Impostiamo l'IP come indice per creare il grafico a barre
            traffic_df.set_index('ip', inplace=True)
            streamlit.bar_chart(traffic_df)
        else:
            streamlit.warning("No device found in the given database. Are you sure scan.py is executing?")