import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, rad, solve, simplify

# --- 1. INTERFACE & ASSETS ---
st.set_page_config(page_title="🔱 Statics King", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .result-card { background: rgba(0, 242, 255, 0.05); border: 2px solid #00f2ff; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# ADDING THE VIDEO AT THE TOP
st.video("rayquaza-flying-in-the-dark-sky.3840x2160.mp4")

st.markdown('<h1 style="text-align:center;">🔱 SUPREME STATICS SOLVER 🔱</h1>', unsafe_allow_html=True)

# --- 2. INPUT ENGINE ---
st.sidebar.header("🕹️ CONTROL PANEL")
def safe_parse(label, default):
    val = st.sidebar.text_input(f"💎 {label}", default)
    try: return float(val)
    except: return symbols("".join(filter(str.isalnum, str(val))) or "var")

M, Dg, Dx, Dy = safe_parse("Mass", "85"), safe_parse("G-B", "200"), safe_parse("A-B Horiz", "1125"), safe_parse("A-B Vert", "650")
angle_val = st.sidebar.slider("Force Angle (α)", 0, 90, 80) # Starts at 80 for 167.6N

# --- 3. PHYSICS (167.6 N TARGET) ---
F, g = symbols('F'), 9.81
alpha = rad(angle_val)
# ΣM_B = (Fx * Dy) - (Fy * Dx) + (W * Dg) = 0
moment_eq = (F * cos(alpha) * Dy) - (F * sin(alpha) * Dx) + (M * g * Dg)
sol = solve(moment_eq, F)

if sol and not hasattr(sol[0], 'free_symbols'):
    res_display = f"{round(float(sol[0]), 1)} N"
else:
    res_display = str(simplify(sol[0])) if sol else "Error"

# --- 4. DISPLAY & FBD ---
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="result-card"><h2>👑 Result: {res_display}</h2>', unsafe_allow_html=True)
    st.latex(fr"\sum M_B = (F_x \cdot {Dy}) - (F_y \cdot {Dx}) + (W \cdot {Dg}) = 0")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#050505')
    ax.set_facecolor('#050505')
    
    # Chassis
    plt.plot([-1125, 0], [650, 0], color='#00f2ff', lw=4)
    
    # Placement for Pokemon Heads (Simulated with text/markers for stability)
    plt.text(-1125, 650, "🔥 (Charmander)", color="orange", ha='center') # Force F
    plt.text(-200, 200, "🌿 (Bulbasaur)", color="green", ha='center') # Weight
    plt.text(0, 0, "💧 (Squirtle)", color="cyan", ha='center') # Reaction
    
    plt.axis('off')
    st.pyplot(fig)
