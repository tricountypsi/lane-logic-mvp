import streamlit as st

# 1. THE DELTA ENGINE LOGIC
def get_advice(result, speed, release):
    # Marcus Filter (Release)
    if release == 'Pulled (PI)':
        return "🎯 PULL DETECTED: Disregard lane friction. Check your target."
    if release == 'Pushed (PO)':
        return "💨 PUSHED: Ball missed out. Do not adjust."

    # Speed Filter
    if speed == 'Fast':
        return "⚠️ SPEED TOO FAST: Stay put. Ball didn't have time to hook."
    if speed == 'Slow':    
        return "⚠️ SPEED TOO SLOW: Stay put. Ball hooked too early."

    # Core Logic
    if result == "High":
        return "📉 Move 1-1 Left (Friction detected)"
    elif result == "Brooklyn":
        return "📉 Move 2-2 Left (Heavy friction)"
    elif result == "Light":
        return "💧 Move 1-0 Right (Oil detected)"
    elif result == "Flush":
        return "✅ Great shot! Stay on this line."
    
    return "Enter shot data for advice."

# 2. UI SETUP
st.set_page_config(page_title="Lane Logic™ MVP", layout="centered")
st.title("🎳 Lane Logic™ Delta Engine")

# 3. INPUTS
st.subheader("1. Result")
result = st.radio("Where did the ball hit?", ["Flush", "High", "Light", "Brooklyn"], horizontal=True)

st.subheader("2. Speed")
speed = st.radio("How was the speed?", ["OK Speed", "Fast", "Slow"], horizontal=True)

st.subheader("3. Release")
release = st.radio("How was the release?", ["Good Release (GR)", "Pulled (PI)", "Pushed (PO)"], horizontal=True)

# 4. DISPLAY ADVICE
st.divider()
advice = get_advice(result, speed, release)

if "🎯" in advice or "⚠️" in advice:
    st.warning(advice)
elif "✅" in advice:
    st.success(advice)
elif "Move" in advice:
    st.info(advice)
else:
    st.write(advice)
