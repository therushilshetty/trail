import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, rad, solve, simplify, Symbol

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Statics Solver Pro", layout="wide")
st.title("🏗️ Ultimate Statics Solver")
st.markdown("---")

# --- 2. THE "ANYTHING" INPUT HANDLER ---
def safe_parse(label, default_val):
    """Ensures ANY input becomes a valid mathematical object."""
    user_input = st.sidebar.text_input(label, default_val)
    # Check if it's a number
    try:
        return float(user_input)
    except ValueError:
        # If it's not a number (like 'm', 'g', 'Force'), turn it into a Math Symbol
        # Clean the string to ensure it's a valid symbol name
        clean_name = "".join(filter(str.isalnum, user_input)) or "var"
        return symbols(clean_name)

# --- 3. SIDEBAR ---
st.sidebar.header("🛠️ System Inputs")
st.sidebar.warning("You can type numbers OR any text (like 'm', 'g', '$$').")

M  = safe_parse("Mass (m)", "85")
Dg = safe_parse("Dist G to B (horiz. mm)", "200")
Dx = safe_parse("Dist A to B (horiz. mm)", "1125")
Dy = safe_parse("Height of A (vert. mm)", "650")

theta_h = st.sidebar.slider("Handle Angle (deg)", 0, 45, 20)
theta_f_rel = st.sidebar.slider("Force F Angle (relative)", 0, 90, 60)

# --- 4. THE BULLETPROOF MATH ---
F = symbols('F')
g_accel = 9.81

# Convert angles using SymPy's version of rad/sin/cos
# This is why your previous code crashed—standard sin() can't handle symbols!
alpha_deg = 90 - (theta_f_rel - theta_h)
alpha_rad = rad(alpha_deg)

# Equation: (F*sin(a)*Dx) + (F*cos(a)*Dy) - (M*g*Dg) = 0
moment_eq = (F * sin(alpha_rad) * Dx) + (F * cos(alpha_rad) * Dy) - (M * g_accel * Dg)

# Solve
solution_list = solve(moment_eq, F)
final_result = simplify(solution_list[0]) if solution_list else "No Solution"

# --- 5. UI DISPLAY ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Mathematical Output")
    # This will display the formula even if the input was 'm' or 'apple'
    st.success("### Required Force F:")
    st.code(str(final_result), language="text")
    
    st.markdown("#### Formula Derivation:")
    st.latex(r"F = \frac{m \cdot g \cdot d_g}{\sin(\alpha)d_x + \cos(\alpha)d_y}")

with col2:
    st.subheader("📐 Free Body Diagram")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Visualization Scale Helper
    def to_f(s): return 1.0 if hasattr(s, 'free_symbols') else s
    
    # Plot basic geometry
    plt.plot([-to_f(Dx), 0], [to_f(Dy), 0], 'o-', color='gray', lw=3)
    plt.axhline(0, color='black', lw=2)
    
    # Draw simplified Force Arrows
    plt.arrow(-to_f(Dx), to_f(Dy), 50, 100, width=10, color='blue', label='F')
    plt.arrow(-to_f(Dg), to_f(Dy)*0.5, 0, -100, width=10, color='red', label='mg')
    
    plt.legend()
    plt.axis('equal')
    plt.axis('off')
    st.pyplot(fig)
