import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import streamlit as st # type: ignore
from weighted_proj_tools import * # type: ignore

pages_path = "./"

home_page = st.Page(f"{pages_path}HomePage.py", title="Home", icon=":material/home:")
weight_reduction_page = st.Page("WeightReductionPage.py", title="Weight Reduction")
degree_reduction_page = st.Page("DegreeReductionPage.py", title="Degree Reduction") #icon=":material/format_list_bulleted:")
dimcalc_page = st.Page(f"{pages_path}DimensionCalculatorPage.py", title="Linear System Dimension Calculator") #, icon=":material/add_circle:")
sheaf_page = st.Page(f"{pages_path}SheafAmplenessPage.py", title="Sheaf Ampleness Checker")
embedding_page = st.Page(f"{pages_path}EmbeddingWPSPage.py", title="Embedding Weighted Projective Space") #, icon=":material/delete:")


pg = st.navigation([home_page, weight_reduction_page, dimcalc_page, embedding_page])#, sheaf_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()


#maybe do multipage as follows :
# one page reduces the weights of weighted projective space
# one page calculates dimension of linear system (also reduces the weights)
# one page calculates the embedding dimension of the weighted projective space
# one page that checks if a sheaf is very ample or not
