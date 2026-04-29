import streamlit as st
import pandas as pd

# 1. THE TRANSLATION & DELTA ENGINE
def get_advice(pins_left, entry_zone, quality, speed, release, history, handedness, sensitivity):
    # Marcus Filter (Release) - Highest priority
    if release == 'Pulled (PI)':
        return "🎯 PULL DETECTED: Disregard lane friction. Check your target.", "warning"
    if release == 'Pushed (PO)':
        return "📌 PUSHED: Ball missed out. Do not adjust.", "warning"

    # Speed Filter
    if speed == 'Fast':
        return "🔥 SPEED TOO FAST: Stay put. Ball didn't have time to hook.", "warning"
    if speed == 'Slow':
        return "🐢 SPEED TOO SLOW: Stay put. Ball hooked too early.", "warning"

    # --- PIN TRANSLATION LOGIC ---
    # Convert Pins to a "Logic Result" (High/Light/Flush)
    result = "Flush"
    if entry_zone == "Brooklyn/Jersey":
        result = "Brooklyn"
    elif not pins_left: # Strike
        result = "Flush"
    else:
        # High Leaves (Righty: 4, 9, 6-10 | Lefty: 6, 8, 4-7)
        high_pins = [4, 9] if handedness == "Right" else [6, 8]
        if any(p in pins_left for p in high_pins) or quality == "High":
            result = "High"
        
        # Light Leaves (Righty: 5, 2, 10-flat | Lefty: 5, 3, 7-flat)
        light_pins = [5, 2] if handedness == "Right" else [5, 3]
        if any(p in pins_left for p in light_pins) or quality == "Light":
            result = "Light"

    # --- MOVEMENT LOGIC ---
    move_dir = "Left" if handedness == "Right" else "Right"
    opp_dir = "Right" if handedness == "Right" else "Left"

    # ENERGY DRAIN (Immediate trigger)
    if len(history) >= 1:
        last_shot = history[-1]
        if last_shot['Logic_Result'] in ['High', 'Brooklyn'] and result == 'Light':
            return "⚡️ CRITICAL: Energy Drain. BALL DOWN NOW.", "error"

    # TRIGGER THRESHOLD (Power vs Stroker)
    trigger_needed = 1 if sensitivity == "Power" else 2
    
    if len(history) >= (trigger_needed - 1):
        # Check if last N shots match the current result
        recent_matches = all(s['Logic_Result'] == result for s in history[-(trigger_needed-1):]) if trigger_needed > 1 else True
        
        if recent_matches:
            if result == "High":
                return f"⬆️ Move 1-1 {move_dir} (Confirmed friction)", "info"
            elif result == "Brooklyn":
                return f"⬆️ Move 2-2 {move_dir} (Heavy transition)", "info"
            elif result == "Light":
                return f"⬇️ Move 1-0 {opp_dir} (Confirmed oil)", "info"

    if result == "Flush":
        return "✅ Great shot! Stay on this line.", "success"

    return "Shot tracked. Watch for a pattern.", "info"

# 2. UI SETUP
st.set_page_config(page_title="Lane Logic™ v1.6", layout="wide")

# Sidebar Configuration
st.sidebar.title("⚙️ System Settings")
handedness = st.sidebar.radio("Handedness:", ["Right", "Left"])
sensitivity = st.sidebar.radio("Player Style:", ["Stroker (Patient)", "Power (Aggressive)"])

st.title("🎳 Lane Logic™ v1.6")
st.caption(f"Active Profile: {handedness}-Handed {sensitivity}")

if 'history' not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Shot Entry")
    
    # Visual Pin Deck (Interactive Checkboxes)
    st.write("Select Pins Left Standing:")
    p_cols = st.columns(4)
    pins = {}
    # Layout pins in a triangle-ish grid
    with p_cols[0]: pins[7] = st.checkbox("7"); pins[4] = st.checkbox("4"); pins[2] = st.checkbox("2"); pins[1] = st.checkbox("1")
    with p_cols[1]: pins[8] = st.checkbox("8"); pins[5] = st.checkbox("5")
    with p_cols[2]: pins[9] = st.checkbox("9"); pins[3] = st.checkbox("3"); pins[6] = st.checkbox("6")
    with p_cols[3]: pins[10] = st.checkbox("10")
    
    selected_pins = [k for k, v in pins.items() if v]

    c1, c2, c3 = st.columns(3)
    with c1:
        entry_zone = st.selectbox("Zone:", ["Pocket", "Brooklyn/Jersey"])
    with c2:
        quality = st.selectbox("Hit Quality:", ["Flush", "High", "Light"])
    with c3:
        speed = st.selectbox("Speed:", ["Good", "Fast", "Slow"])
    
    release = st.selectbox("Release (The Marcus Filter):", ["Good", "Pulled (PI)", "Pushed (PO)"])

    if st.button("Analyze Shot", use_container_width=True):
        advice, advice_type = get_advice(selected_pins, entry_zone, quality, speed, release, st.session_state.history, handedness, sensitivity)
        
        if advice_type == "info": st.info(advice)
        elif advice_type == "warning": st.warning(advice)
        elif advice_type == "error": st.error(advice)
        elif advice_type == "success": st.success(advice)
            
        # Logic_Result is the "translated" result used for math
        res_map = get_advice(selected_pins, entry_zone, quality, speed, release, [], handedness, sensitivity) # Get logic result
        
        # Temp trick to get result string
        temp_res = "Flush"
        if entry_zone == "Brooklyn/Jersey": temp_res = "Brooklyn"
        elif selected_pins:
            if quality == "High": temp_res = "High"
            elif quality == "Light": temp_res = "Light"
        
        st.session_state.history.append({
            "Pins": str(selected_pins) if selected_pins else "Strike",
            "Logic_Result": temp_res,
            "Release": release
        })

with col2:
    st.subheader("Session History")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df.tail(8))
    else:
        st.write("Awaiting first shot...")

    if st.button("Clear Session"):
        st.session_state.history = []
        st.rerun()
