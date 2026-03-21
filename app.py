import streamlit as st
import pandas as pd

# 1. THE DELTA ENGINE LOGIC
def get_advice(result, speed, release, history):
    # Marcus Filter (Release) - Higher priority
    if release == 'Pulled (PI)':
        return "🎯 PULL DETECTED: Disregard lane friction. Check your target.", "warning"
    if release == 'Pushed (PO)':
        return "💨 PUSHED: Ball missed out. Do not adjust.", "warning"

    # Speed Filter - Higher priority
    if speed == 'Fast':
        return "⚠️ SPEED TOO FAST: Stay put. Ball didn't have time to hook.", "warning"
    if speed == 'Slow':
        return "⚠️ SPEED TOO SLOW: Stay put. Ball hooked too early.", "warning"

    # ENERGY DRAIN LOGIC (Three-Shot Pattern)
    if len(history) >= 1:
        last_shot = history[-1]
        if last_shot['Result'] in ['High', 'Brooklyn'] and result == 'Light':
            return "🚨 CRITICAL: Energy Drain. BALL DOWN NOW.", "error"

    # Core Tactical Logic
    if result == "High":
        return "📉 Move 1-1 Left (Friction detected)", "info"
    elif result == "Brooklyn":
        return "📉 Move 2-2 Left (Heavy friction)", "info"
    elif result == "Light":
        return "💧 Move 1-0 Right (Oil detected)", "info"
    elif result == "Flush":
        return "✅ Great shot! Stay on this line.", "success"
    
    return "Enter shot data for advice.", "info"

# 2. UI SETUP
st.set_page_config(page_title="Lane Logic™ MVP v1.4", layout="centered")
st.title("🎳 Lane Logic™ Delta Engine")

# Initialize Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. INPUTS
st.subheader("Current Shot Data")
result = st.radio("1. Result", ["Flush", "High", "Light", "Brooklyn"], horizontal=True)
speed = st.radio("2. Speed", ["OK Speed", "Fast", "Slow"], horizontal=True)
release = st.radio("3. Release", ["Good Release (GR)", "Pulled (PI)", "Pushed (PO)"], horizontal=True)

# 4. ACTION BUTTON
st.divider()
if st.button("SAVE SHOT & GET ADVICE", use_container_width=True):
    advice, alert_type = get_advice(result, speed, release, st.session_state.history)
    
    # Store in history
    st.session_state.history.append({
        "Shot": len(st.session_state.history) + 1,
        "Result": result,
        "Speed": speed,
        "Release": release,
        "Advice": advice
    })
    
    # Show current advice
    if alert_type == "warning": st.warning(advice)
    elif alert_type == "error": st.error(advice)
    elif alert_type == "success": st.success(advice)
    else: st.info(advice)

# 5. SESSION HISTORY
if st.session_state.history:
    st.subheader("Game Log (Last 5 Shots)")
    df = pd.DataFrame(st.session_state.history).tail(5)
    st.table(df)
    
    if st.sidebar.button("Clear Game Data"):
        st.session_state.history = []
        st.rerun()
