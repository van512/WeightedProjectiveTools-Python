import streamlit as st # type: ignore
import re
from weighted_proj_tools import * # type: ignore
import numpy as np # type: ignore

st.title("Weight Reduction")


# Input fields
weights_input = st.text_input("Enter the weights $(a_0, \\dots, a_r$), $(a_i>0)$ :")


if st.button("Calculate"):
    try:
        a = list(map(int, re.split(r'[ ,;:]+', weights_input.strip())))  # Allow spaces, commas, semicolons, or colons as separators 
        if any(int(ai) <= 0 for ai in a):
            st.error("All weights must be greater than $0$. $(" + ",".join(map(str, a)) + ")$ is not a valid weight.")

        else:
            w = Weights(a) # type: ignore

            if w.is_wellformed():
                st.write("The weight $(" + ",".join(map(str, w.weights)) + ")$ is already well-formed.")
                st.write("No reduction needed.")
                st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})$ is a well-formed weighted projective space.")


            else:
                if w.is_reduced():
                    st.write(f"The weight $(" + ",".join(map(str, w.weights)) + ")$ is reduced but not well-formed.")
                    st.write(f"Its associated well-formed weight is $(" + ",".join(map(str, w.wellformed_weights)) + ")$.")
                    st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
                else:
                    st.write(f"The weight $(" + ",".join(map(str, w.weights)) + ")$ is not reduced nor well-formed.")
                    if Weights(w.reduced_weights).is_wellformed(): # type: ignore
                        st.write(f"Its reduced weight is $(" + ",".join(map(str, w.reduced_weights)) + ")$ which is already well-formed.")
                        st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
                    else:
                        st.write(f"Its reduced weight is $(" + ",".join(map(str, w.reduced_weights)) + ")$ and its associated well-formed weight is $(" + ",".join(map(str, w.wellformed_weights)) + ")$.")
                        st.write(f"Hence, $\\mathbb{{P}}({','.join(map(str, w.weights))})= \\mathbb{{P}}({','.join(map(str, w.reduced_weights))})= \\mathbb{{P}}({','.join(map(str, w.wellformed_weights))})$.")
        
    except ValueError:
        st.error("Error: Please enter at least two positive integers.")
