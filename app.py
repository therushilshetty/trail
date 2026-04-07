import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, cos, sin, rad, solve, simplify

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Statics Solver Pro", layout="wide")

st.title("🏗️ Engineering Statics: Wheelbarrow Solver")
st.markdown("""
**Author:** [Your Name]  
**Problem 2/40:** Moment Equilibrium at Point B.  
*This solver uses a Symbolic Math Engine to handle both numerical values and algebraic variables.*
""")
st.write("---")

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("🛠️ System Parameters")
st.sidebar.info("Tip: You can enter numbers (e.g. 85) or symbols (e.g. 'm' or '$').")

# Inputs as strings to allow for symbols
m_in = st.sidebar.text_input("Mass of Load (kg or symbol)", "85")
dg_in = st.sidebar.text_input("Dist G to B (horiz. mm)", "200")
ax_in = st.sidebar.text_input("Dist A to B (horiz. mm)", "1125")
ay_in = st.sidebar.text_input("Height of A (vert. mm)", "650")

st.sidebar.subheader("Fixed Geometry")
theta_h = st.sidebar.slider("Handle Angle (deg)", 0, 45, 20)
theta_f_rel = st.sidebar.slider("Force F Angle relative to handle (deg)", 0, 90, 60)

# --- 3. SYMBOLIC CORE LOGIC ---
# Define the unknown Force as a mathematical symbol
F = symbols('F')
g_accel = 9.81

# Helper function to convert input to Float or Symbol
def parse_input(val):
    try:
        return float(val)
    except:
        return symbols(val)

# Parse all inputs
M = parse_input(m_in)
Dg = parse_input(dg_in)
Dx = parse_input(ax_in)
Dy = parse_input(ay_in)

# Physics: Calculate absolute angle of F from horizontal
# Based on diagram: 90 - (Relative Angle - Handle Angle)
alpha_deg = 90 - (theta_f_rel - theta_h)
alpha_rad = rad(alpha_deg) # Convert to radians using SymPy's rad

# MOMENT EQUATION: Sum of Moments about B = 0 (Counter-Clockwise is positive)
# Equation: (F_y * Dx) + (F_x * Dy) - (Weight * Dg) = 0
moment_eq = (F * sin(alpha_rad) * Dx) + (F * cos(alpha_rad) * Dy) - (M * g_accel * Dg)

# Solve for F
f_solution = solve(moment_eq, F)
final_f = simplify(f_solution[0]) if f_solution else "Error"

# --- 4. DISPLAY RESULTS & FBD ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("✅ Calculated Results")
    st.success(f"**Required Force F:**")
    st.code(f"{final_f}", language="text")
    
    st.markdown("### Derived Formulas")
    st.write("Using $\sum M_B = 0$:")
    st.latex(r"F (\sin \alpha \cdot d_x + \cos \alpha \cdot d_y) = m \cdot g \cdot d_g")
    
    st.info(f"**Current Angle α (from horiz):** {alpha_deg}°")

with col2:
    st.subheader("📐 Free Body Diagram (FBD)")
    
    # Visualization setup
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scale helper for symbols (defaults to 1.0 if not a number)
    def to_val(s): return 1.0 if hasattr(s, 'free_symbols') and s.free_symbols else s
    
    # Coordinates
    pt_A = (-to_val(Dx), to_val(Dy))
    pt_G = (-to_val(Dg), to_val(Dy) * 0.4)
    pt_B = (0, 0)

    # 1. Draw Ground and Frame
    plt.axhline(0, color='black', lw=1.5, ls='--')
    plt.plot([pt_A[0], pt_B[0]], [pt_A[1], pt_B[1]], color='gray', lw=4, alpha=0.6, label="Frame")

    # 2. Draw Forces (Quivers)
    # Applied Force F at A
    plt.quiver(pt_A[0], pt_A[1], 0.3, 0.8, color='#1f77b4', scale=5, label='Applied Force F')
    # Weight mg at G
    plt.quiver(pt_G[0], pt_G[1], 0, -1.2, color='#d62728', scale=5, label='Weight (mg)')
    # Reaction at B
    plt.quiver(0, 0, 0, 1, color='#2ca02c', scale=5, label='Normal Reaction (N)')

    # 3. Annotations
    plt.text(pt_A[0], pt_A[1]+50, 'A', fontweight='bold', fontsize=12)
    plt.text(pt_G[0], pt_G[1]+50, 'G', fontweight='bold', fontsize=12)
    plt.text(5, 5, 'B (Pivot)', fontweight='bold', fontsize=12)

    plt.axis('equal')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    st.pyplot(fig)

st.write("---")
st.caption("Developed for Engineering Mechanics: Statics - Assignment Component")
