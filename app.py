import streamlit as st

import pandas as pd

# 1. THE DELTA ENGINE LOGIC

class DeltaEngine:

    def analyze_shot(self, result, speed, pocket, history):

        if speed in ['Fast', 'Slow']:

            return "⚠️ SPEED ERROR: Stay put. Do not adjust.", "warning"

        

        # Energy Drain Rule

        if len(history) >= 1:

            prev = history[-1]

            if prev['result'] in ['High', 'Brooklyn'] and result == 'Light':

                return "🚨 CRITICAL: Energy Drain. BALL DOWN NOW.", "error"

        # Basic Transition Logic

        if result in ['High', 'Brooklyn']:

            return "📉 CAUTION: Friction detected. Move 1-1 Left.", "info"

        elif result == 'Light':

            return "💧 OIL DETECTED: Ball finishing late. Move 1-0 Right.", "info"

        

        return "✅ STATUS: Stable. Stay on this line.", "success"

# 2. STREAMLIT UI SETUP

st.set_page_config(page_title="Lane Logic™ MVP", layout="centered")

st.title("🎳 Lane Logic™ Delta Engine")

if 'history' not in st.session_state:

    st.session_state.history = []

# 3. SIDEBAR: ARSENAL & SETTINGS

with st.sidebar:

    st.header("Setup")

    ball = st.selectbox("Current Ball", ["Phaze II Solid", "Phaze II Pearl", "Hustle X-Ray"])

    st.divider()

    if st.button("Reset Session"):

        st.session_state.history = []

        st.rerun()

# 4. MAIN INTERFACE: INPUT BUTTONS

st.subheader("Last Shot Result")

col1, col2, col3, col4 = st.columns(4)

with col1: res = "Flush" if st.button("Flush 🟢") else None

with col2: res = "High" if st.button("High 🔴") else None

with col3: res = "Light" if st.button("Light 🟡") else None

with col4: res = "Brooklyn" if st.button("BK 🔵") else None

st.subheader("Speed Filter")

s_col1, s_col2, s_col3 = st.columns(3)

with s_col1: spd = "OK" if st.button("OK Speed") else None

with s_col2: spd = "Fast" if st.button("FAST") else None

with s_col3: spd = "Slow" if st.button("SLOW") else None

# 5. PROCESS & ADVISE

if res and spd:

    engine = DeltaEngine()

    msg, type = engine.analyze_shot(res, spd, "Mid", st.session_state.history)

    

    st.session_state.history.append({"ball": ball, "result": res, "speed": spd, "advice": msg})

    

    # Big Advisor Box

    if type == "success": st.success(msg)

    elif type == "info": st.info(msg)

    elif type == "warning": st.warning(msg)

    else: st.error(msg)

# 6. HISTORY LOG

if st.session_state.history:

    st.divider()

    st.subheader("Session Log")

    df = pd.DataFrame(st.session_state.history)

    st.table(df.tail(5))
