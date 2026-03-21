import streamlit as st
    import pandas as pd
    
    # 1. THE DELTA ENGINE LOGIC
    class DeltaEngine:
        def analyze_shot(self, result, speed, release, history):
            if speed in ['Fast', 'Slow']:
                return "⚠️ SPEED ERROR: Stay put. Do not adjust.", "warning"
            
            if release == 'Pulled':
                return "🎯 PULL DETECTED: Disregard lane friction. Check your target.", "warning"
            
            # Energy Drain Rule
            if len(history) >= 1:
                prev = history[-1]
                if prev.get('result') in ['High', 'Brooklyn'] and result == 'Light':
                    return "🚨 CRITICAL: Energy Drain. BALL DOWN NOW.", "error"
    
            # Basic Transition Logic
            if result in ['High', 'Brooklyn']:
                return "📉 CAUTION: Friction detected. Move 1-1 Left.", "info"
            elif result == 'Light':
                return "💧 OIL DETECTED: Ball finishing late. Move 1-0 Right.", "info"
            
            return "✅ STATUS: Stable. Stay on this line.", "success"
    
    # 2. UI SETUP & STATE
    st.set_page_config(page_title="Lane Logic™ MVP v1.2", layout="centered")
    st.title("🎳 Lane Logic™ Delta Engine")
    
    if 'history' not in st.session_state: st.session_state.history = []
    if 'last_res' not in st.session_state: st.session_state.last_res = None
    if 'last_spd' not in st.session_state: st.session_state.last_spd = None
    if 'last_rel' not in st.session_state: st.session_state.last_rel = "Good"
    
    # 3. SIDEBAR
    with st.sidebar:
        st.header("Setup")
        ball = st.selectbox("Current Ball", ["Phaze II Solid", "Phaze II Pearl", "Hustle X-Ray"])
        if st.button("Reset Session"):
            st.session_state.history = []
            st.session_state.last_res = None
            st.rerun()
    
    # 4. INPUT BUTTONS
    st.subheader("1. Result")
    r1, r2, r3, r4 = st.columns(4)
    if r1.button("Flush 🟢"): st.session_state.last_res = "Flush"
    if r2.button("High 🔴"): st.session_state.last_res = "High"
    if r3.button("Light 🟡"): st.session_state.last_res = "Light"
    if r4.button("BK 🔵"): st.session_state.last_res = "Brooklyn"
    
    st.subheader("2. Speed")
    s1, s2, s3 = st.columns(3)
    if s1.button("OK Speed"): st.session_state.last_spd = "OK"
    if s2.button("FAST"): st.session_state.last_spd = "Fast"
    if s3.button("SLOW"): st.session_state.last_spd = "Slow"
    
    st.subheader("3. Release")
    rel1, rel2 = st.columns(2)
    if rel1.button("Good Release (GR)"): st.session_state.last_rel = "Good"
    if rel2.button("Pulled (PI)"): st.session_state.last_rel = "Pulled"
    
    # 5. PROCESS & DISPLAY ADVICE
    if st.session_state.last_res and st.session_state.last_spd:
        engine = DeltaEngine()
        msg, alert_type = engine.analyze_shot(
            st.session_state.last_res, 
            st.session_state.last_spd, 
            st.session_state.last_rel, 
            st.session_state.history
        )
        
        # Show the Big Advice Box
        if alert_type == "success": st.success(msg)
        elif alert_type == "info": st.info(msg)
        elif alert_type == "warning": st.warning(msg)
        else: st.error(msg)
        
        # Save to history and reset for next shot
        if st.button("Confirm & Save Shot"):
            st.session_state.history.append({
                "ball": ball, 
                "result": st.session_state.last_res, 
                "speed": st.session_state.last_spd, 
                "advice": msg
            })
            st.session_state.last_res = None
            st.session_state.last_spd = None
            st.rerun()
    
    # 6. LOG
    if st.session_state.history:
        st.divider()
        st.subheader("Session Log")
        st.table(pd.DataFrame(st.session_state.history).tail(5))
    
