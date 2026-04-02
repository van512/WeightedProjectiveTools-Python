import streamlit as st # type: ignore
import re
from weighted_proj_tools import * # type: ignore
import numpy as np # type: ignore

st.title("Degree Reduction")

def trigger_calculation():
    st.session_state.run_calc = True

# Input fields
st.text_input(
    "Enter the weights $(a_0, \\dots, a_r)$ as positive integers (separated by spaces, commas, or other common separators):", 
    placeholder="e.g. 2 3 10 15 or 1, 4, 9", 
    help="Enter positive integers separated by spaces, commas, semicolons, colons or full points. For example: 2, 3; 10: 15 or 2 3 10 15.Enter the weights (a_0, ..., a_n) separated by spaces or commas (a_i > 0):",
    key="weights_input",
)

st.text_input(
    "Enter the degree $d$:", 
    placeholder="e.g 30 or 67", 
    key="degree_input",
    on_change=trigger_calculation
)

if st.button("Calculate"):
    trigger_calculation()

# Run calculation only when triggered
if st.session_state.get("run_calc", False):
    try:
        a = list(map(int, re.split(r'[ ,;:.]+', st.session_state.weights_input.strip())))  # Allow spaces, commas, semicolons, or colons as separators 
        if any(int(ai) <= 0 for ai in a):
            st.error("All weights must be positive integers. $(" + ",".join(map(str, a)) + ")$ is not a valid weight.")

        d = st.session_state.degree_input.strip()
        if not d.isdigit() or int(d) <= 0:
            st.error("The degree $d$ must be a positive integer.")
        
        #
        w = Weights(a) # type: ignore

        if w.is_wellformed():
            st.write("The weight $a'=(" + ",".join(map(str, w.weights)) + ") = a = \\bar{{a}}$ is already well-formed.")
            st.write("No reduction needed.")
            st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})$ is a well-formed weighted projective space.")


        else:
            if w.is_reduced():
                st.write(f"The weight $a'= (" + ",".join(map(str, w.weights)) + ") = a$ is reduced but not well-formed.")
                st.write(f"Its associated well-formed weight is $\\bar{{a}} = (" + ",".join(map(str, w.wellformed_weights)) + ")$.")
                st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
            else:
                st.write(f"The weight $a'=(" + ",".join(map(str, w.weights)) + ")$ is not reduced nor well-formed.")
                if Weights(w.reduced_weights).is_wellformed(): # type: ignore
                    st.write(f"Its reduced weight is $a = (" + ",".join(map(str, w.reduced_weights)) + ") = \\bar{{a}}$ which is already well-formed.")
                    st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
                else:
                    st.write(f"Its reduced weight is $a = (" + ",".join(map(str, w.reduced_weights)) + ")$ and its associated well-formed weight is $ \\bar{{a}} = (" + ",".join(map(str, w.wellformed_weights)) + ")$.")
                    st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.reduced_weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
    
    except ValueError:
        st.error("Error: Please enter at least two positive integers.")



st.markdown("---")

# Explanation of degree reduction
st.markdown(r"""
### What is Degree Reduction?

In algebraic geometry, **degree reduction** simplifies the weights that define a weighted projective space $\mathbb{P}(a_0,\dots,a_r)$ in two steps:

1. **Reduction**: Remove common factors from all weights so that $\gcd(a_0,\dots,a_r) = 1$. The resulting weight is called **reduced**, denoted $a$.
2. **Well-Forming**: Adjust weights so that any $r-1$ of them are coprime, i.e., $s_i=\gcd(a_0,\dots,\hat{a_i},\dots,a_r) = 1$ for all $i$. The resulting weight is called **well-formed**, denoted $\bar{a}$.

Thanks to theorems in the literature (e.g. **Beltrametti–Robbiano**), these transformations preserve the space up to isomorphism:
$$
\mathbb{P}(a') \simeq \mathbb{P}(a) \simeq \mathbb{P}(\bar{a})
$$

- $a'$ is the **arbitrary weight** you input,
- $a$ is the **reduced weight** (after removing common divisors),
- $\bar{a}$ is the **well-formed weight** (after making all $s_i = 1$).

So we can always assume the space is **well-formed** without loss of generality.
""")