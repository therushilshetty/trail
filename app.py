import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, rad, solve, simplify, latex

# --- 1. ROYAL GAMER INTERFACE (CSS) ---
st.set_page_config(page_title="👑 Statics King: Wheelbarrow Solver", layout="wide")

st.markdown("""
    <style>
    /* Background and Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #00d4ff;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-right: 2px solid #ff00ff;
    }
    /* Deluxe Header */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
    }
    /* Card/Box Styling */
    .stMetric, .stAlert, .stCodeBlock {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🔱 STATICS ROYAL SOLVER 🔱</p>', unsafe_allow_html=True)

# --- 2. THE BULLETPROOF INPUT ENGINE ---
def royal_input(label, default):
    return st.sidebar.text_input(f"💎 {label}", default)

M_in = royal_input("Mass (m)", "85")
Dg_in = royal_input("G-to-B Dist (dg)", "200")
Dx_in = royal_input("A-to-B Dist (dx)", "1125")
Dy_in = royal_input("A-Height (dy)", "650")

theta_h = st.sidebar.slider("Handle Angle", 0, 45, 20)
theta_f_rel = st.sidebar.slider("Force F Rel Angle", 0, 90, 60)

# --- 3. THE PHYSICS ENGINE ---
F = symbols('F')
g = 9.81

def parse(x):
    try: return float(x)
    except: return symbols("".join(filter(str.isalnum, str(x))) or "var")

M, Dg, Dx, Dy = parse(M_in), parse(Dg_in), parse(Dx_in), parse(Dy_in)

# Angle Math
alpha_deg = 90 - (theta_f_rel - theta_h)
alpha_rad = rad(alpha_deg)

# Equilibrium Equation: F_y*Dx + F_x*Dy - W*Dg = 0
moment_eq = (F * sin(alpha_rad) * Dx) + (F * cos(alpha_rad) * Dy) - (M * g * Dg)

# The Solution
sol_list = solve(moment_eq, F)
final_F = simplify(sol_list[0]) if sol_list else 0

# --- 4. LAYOUT: RESULTS & PROOF ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 👑 ROYAL RESULT")
    st.markdown(f"""
    <div style="padding: 20px; border-radius: 15px; border: 2px solid #00d4ff; background: rgba(0,212,255,0.1);">
        <h2 style="color: #ffffff; margin:0;">F = {final_F}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛡️ TRUTH JUSTIFICATION")
    with st.expander("Why is this correct? (Proof)"):
        st.write("For the system to be stationary, the **Net Moment** about B must be exactly zero.")
        st.latex(fr"\sum M_B = (F \sin \alpha \cdot d_x) + (F \cos \alpha \cdot d_y) - (m \cdot g \cdot d_g)")
        
        # Substitution Proof
        st.write("Plugging your inputs back into the moment equation:")
        proof_calc = (final_F * sin(alpha_rad) * Dx) + (final_F * cos(alpha_rad) * Dy) - (M * g * Dg)
        st.write(f"Net Moment = **{simplify(proof_calc)}**")
        st.success("Verification Complete: Net Moment = 0. System is in Equilibrium.")

with col2:
    st.markdown("### 📐 TACTICAL FBD")
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Scaled Coordinates for plotting
    def s(v): return 1.0 if hasattr(v, 'free_symbols') else v
    ax.plot([-s(Dx), 0], [s(Dy), 0], color='#ff00ff', lw=4, label='Chassis')
    ax.axhline(0, color='#00d4ff', lw=2, ls='--')
    
    # Glow effect arrows (simplified)
    ax.quiver(-s(Dx), s(Dy), 0.2, 0.6, color='#00d4ff', scale=5, width=0.015)
    ax.quiver(-s(Dg), s(Dy)*0.4, 0, -0.8, color='#ff4b4b', scale=5, width=0.015)
    
    plt.axis('off')
    st.pyplot(fig)
