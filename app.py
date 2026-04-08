import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, rad, solve, simplify
import os

# --- 1. THEME SETTINGS ---
st.set_page_config(page_title="🔱 Statics King", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #00f2ff; font-family: 'Courier New', Courier, monospace; }
    .result-card { background: rgba(0, 242, 255, 0.1); border: 2px solid #00f2ff; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VIDEO HANDLER (FIXES THE RED BOX ERROR) ---
video_filename = "rayquaza-flying-in-the-dark-sky.3840x2160.mp4"

# Safety check: Shows an info box instead of a crash if the video is missing
if os.path.exists(video_filename):
    st.video(video_filename)
else:
    st.info(f"📽️ Video '{video_filename}' not detected on GitHub. Upload it to remove this message.")

st.markdown('<h1 style="text-align:center;">🔱 SUPREME STATICS SOLVER 🔱</h1>', unsafe_allow_html=True)

# --- 3. SYMBOLIC INPUT ENGINE (FIXES THE TYPEERROR) ---
st.sidebar.header("🕹️ CONTROL PANEL")

def safe_input(label, default):
    val = st.sidebar.text_input(f"💎 {label}", default)
    try:
        return float(val) # If it's a number, use it
    except ValueError:
        # If it's a letter (m, g, a), make it a math symbol so it doesn't crash
        return symbols("".join(filter(str.isalnum, str(val))) or "var")

M = safe_input("Mass of Load", "85")
Dg = safe_input("Dist G to B (horiz)", "200")
Dx = safe_input("Dist A to B (horiz)", "1125")
Dy = safe_input("Height of A (vert)", "650")

# Your verified 80° logic for the 167.6 N result
alpha = rad(80) 

# --- 4. MATH ENGINE ---
F = symbols('F')
g_constant = 9.81

# Moment Equation about B
moment_eq = (F * cos(alpha) * Dy) - (F * sin(alpha) * Dx) + (M * g_constant * Dg)

sol = solve(moment_eq, F)

# Display Logic
if sol:
    if not hasattr(sol[0], 'free_symbols'):
        ans = f"{round(float(sol[0]), 1)} N"
    else:
        ans = str(simplify(sol[0]))
else:
    ans = "No Solution"

# --- 5. OUTPUT ---
st.markdown(f'<div class="result-card"><h2>👑 Calculated Force: {ans}</h2></div>', unsafe_allow_html=True)

# --- 6. TACTICAL FBD ---
fig, ax = plt.subplots()
fig.patch.set_facecolor('#050505')
ax.set_facecolor('#050505')
plt.plot([-1125, 0], [650, 0], color='#00f2ff', lw=5) # Chassis
plt.text(-1125, 650, "🔥 (F)", color="orange", fontsize=12) # Charmander/Force
plt.text(-200, 300, "🌿 (W)", color="green", fontsize=12) # Bulbasaur/Weight
plt.text(0, 0, "💧 (R)", color="cyan", fontsize=12) # Squirtle/Reaction
plt.axis('off')
st.pyplot(fig)
