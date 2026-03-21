import streamlit as st
import pandas as pd
    
    # 1. THE DELTA ENGINE LOGIC
    def get_advice(result, speed, release, history):
        # Marcus Filter (Release) - Highest priority
        if release == 'Pulled (PI)':
            return "🎯 PULL DETECTED: Disregard lane friction. Check your target.", "warning"
        if release == 'Pushed (PO)':
            return "💨 PUSHED: Ball missed out. Do not adjust.", "warning"
    
        # Speed Filter - High priority
        if speed == 'Fast':
            return "⚠️ SPEED TOO FAST: Stay put. Ball didn't have time to hook.", "warning"
        if speed == 'Slow':
            return "⚠️ SPEED TOO SLOW: Stay put. Ball hooked too early.", "warning"
    
        # ENERGY DRAIN LOGIC (Immediate trigger)
        if len(history) >= 1:
            last_shot = history[-1]
            if last_shot['Result'] in ['High', 'Brooklyn'] and result == 'Light':
                return "🚨 CRITICAL: Energy Drain. BALL DOWN NOW.", "error"
    
        # PATIENCE LOGIC (Requires 2 consecutive misses to suggest a move)
        if len(history) >= 1:
            last_shot = history[-1]
            if last_shot['Result'] == result:
                if result == "High":
                    return "📉 Move 1-1 Left (Confirmed friction)", "info"
                elif result == "Brooklyn":
                    return "📉 Move 2-2 Left (Confirmed heavy friction)", "info"
                elif result == "Light":
                    return "💧 Move 1-0 Right (Confirmed oil)", "info"
        
        if result == "Flush":
            return "✅ Great shot! Stay on this line.", "success"
        
        return "Shot tracked. Watch for a pattern.", "info"
    
    # 2. UI SETUP
    st.set_page_config(page_title="Lane Logic™ MVP v1.5", layout="centered")
    st.title("🎳 Lane Logic™ Delta Engine")
    
    # Initialize Session State
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    # 3. INPUTS
    st.subheader("Current Shot Data")
    # Use a dynamic key to reset radio buttons
    k = st.session_state.input_key
    result = st.radio("1. Result", ["Flush", "High", "Light", "Brooklyn"], horizontal=True, key=f"res_{k}")
    speed = st.radio("2. Speed", ["OK Speed", "Fast", "Slow"], horizontal=True, key=f"spd_{k}")
    release = st.radio("3. Release", ["Good Release (GR)", "Pulled (PI)", "Pushed (PO)"], horizontal=True, key=f"rel_{k}")
    
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
        
        # Increment key to reset UI inputs for next shot
        st.session_state.input_key += 1
        
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
            st.session_state.input_key = 0
            st.rerun()
    
