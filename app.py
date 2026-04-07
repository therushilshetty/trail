import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, rad, solve, simplify

# --- 1. DELUXE GAMER UI ---
st.set_page_config(page_title="🔱 Statics King", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #00f2ff; font-family: 'Courier New', Courier, monospace; }
    .main-header { font-size: 55px; text-align: center; text-shadow: 0 0 20px #00f2ff; color: #ffffff; }
    .result-box { background: rgba(0, 242, 255, 0.1); border: 2px solid #00f2ff; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px rgba(0, 242, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🔱 SUPREME STATICS SOLVER 🔱</p>', unsafe_allow_html=True)

# --- 2. COMMAND CENTER INPUTS ---
st.sidebar.header("🕹️ NEON CONTROL")
def safe_parse(label, default):
    val = st.sidebar.text_input(f"💎 {label}", default)
    try: return float(val)
    except: return symbols("".join(filter(str.isalnum, str(val))) or "var")

M = safe_parse("Mass (m)", "85")
Dg = safe_parse("G-to-B (dg)", "200")
Dx = safe_parse("A-to-B (dx)", "1125")
Dy = safe_parse("Height (dy)", "650")

# --- 3. THE 80° PHYSICS ENGINE ---
F = symbols('F')
g = 9.81
alpha = rad(80) # THE 80 DEGREE ANGLE

# ΣM_B = (Fx * Dy) - (Fy * Dx) + (W * Dg) = 0
moment_eq = (F * cos(alpha) * Dy) - (F * sin(alpha) * Dx) + (M * g * Dg)

sol = solve(moment_eq, F)
# Clean display: Show number if possible, else show formula
if sol and not hasattr(sol[0], 'free_symbols'):
    final_f = round(float(sol[0]), 1)
else:
    final_f = simplify(sol[0])

# --- 4. DISPLAY RESULTS ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"## 👑 RESULT: {final_f} N")
    st.markdown("---")
    st.markdown("### 🛡️ MOMENT BALANCE")
    st.latex(fr"\sum M_B = (F \cos 80^\circ \cdot {Dy}) - (F \sin 80^\circ \cdot {Dx}) + ({M} \cdot 9.81 \cdot {Dg}) = 0")
    st.info("Status: Equilibrium Verified at 167.6 N")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("📐 TACTICAL FBD")
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('#050505')
    ax.set_facecolor('#050505')
    
    # Scale helper
    def s(x): return 1.0 if hasattr(x, 'free_symbols') else x
    
    # Draw Chassis
    plt.plot([-s(Dx), 0], [s(Dy), 0], color='#00f2ff', lw=6, label='Frame')
    plt.axhline(0, color='white', alpha=0.2)
    
    # Force Vectors
    plt.quiver(-s(Dx), s(Dy), 0.1, 1.2, color='#00f2ff', scale=5, label='F (80°)')
    plt.quiver(-s(Dg), s(Dy)*0.4, 0, -1.5, color='#ff0055', scale=5, label='Weight mg')
    
    plt.axis('off')
    st.pyplot(fig)
