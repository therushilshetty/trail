import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, cos, sin, rad, solve, simplify

# --- UI Header ---
st.set_page_config(page_title="Statics Solver Pro", page_icon="🏗️")
st.title("🏗️ Professional Statics: Wheelbarrow Solver")
st.markdown("---")

# --- Sidebar for Inputs ---
st.sidebar.header("📝 Input Parameters")
st.sidebar.info("You can enter numbers (85) or variables (m, $, L).")

m_in = st.sidebar.text_input("Mass (m)", "85")
dg_in = st.sidebar.text_input("Dist G to B (horiz mm)", "200")
ax_in = st.sidebar.text_input("Dist A to B (horiz mm)", "1125")
ay_in = st.sidebar.text_input("Height of A (vert mm)", "650")

# Sliders for interactive feel
st.sidebar.subheader("Geometry")
theta_h = st.sidebar.slider("Handle Angle (°)", 0, 45, 20)
theta_f = st.sidebar.slider("F angle relative to handle (°)", 0, 90, 60)

# --- Math Logic ---
F, g = symbols('F g'), 9.81
def parse(x):
    try: return float(x)
    except: return symbols(x)

M, Dx, Dy, Dg = parse(m_in), parse(ax_in), parse(ay_in), parse(dg_in)
alpha = rad(90 - (theta_f - theta_h))

# Equilibrium: Sum of Moments about B = 0
moment_eq = (F * sin(alpha) * Dx) + (F * cos(alpha) * Dy) - (M * 9.81 * Dg)
solution = solve(moment_eq, F)[0]

# --- Layout: Results & FBD ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✅ Calculated Force F")
    st.success(f"**F =** {simplify(solution)}")
    
    st.markdown("### Equilibrium Equations")
    st.latex(r"\sum M_B = 0")
    st.latex(r"(F \sin \alpha \cdot d_x) + (F \cos \alpha \cdot d_y) - (mg \cdot d_g) = 0")

with col2:
    st.subheader("📐 Free Body Diagram")
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Simple logic to scale the plot if inputs are symbols
    def get_val(s): return 1.0 if hasattr(s, 'free_symbols') and s.free_symbols else s
    
    # Drawing the "Wheelbarrow"
    A = (-get_val(Dx), get_val(Dy))
    G = (-get_val(Dg), get_val(Dy)*0.4)
    B = (0, 0)
    
    plt.plot([A[0], B[0]], [A[1], B[1]], color='black', lw=3, label="Frame")
    plt.axhline(0, color='gray', lw=1, ls='--') # Ground
    
    # Adding Vectors (FBD)
    plt.quiver(A[0], A[1], 0.3, 0.8, color='blue', scale=5, label='Force F')
    plt.quiver(G[0], G[1], 0, -1, color='red', scale=5, label='Weight mg')
    plt.quiver(0, 0, 0, 0.8, color='green', scale=5, label='Normal Force')
    
    plt.legend()
    plt.axis('off')
    st.pyplot(fig)
