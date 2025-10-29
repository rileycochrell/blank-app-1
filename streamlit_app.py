import streamlit as st

st.title("Environmental Justice Index Visualization (NM)")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
    options = ["Option A", "Option B", "Option C"]
    selected_option = st.selectbox("Choose an option:", options)
    st.write(f"You selected: {selected_option}")
    if option == "Option A":
        st.write("You selected Option A. Here is some content specific to Option A.")
        # You can add more Streamlit widgets here, like st.text_input, st.button, etc.
        st.image("https://via.placeholder.com/150", caption="Image for Option A")
    elif option == "Option B":
        st.write("You selected Option B. This content is for Option B.")
        st.dataframe({"Column 1": [1, 2], "Column 2": ["X", "Y"]})
    else:
        st.write("You selected Option C. Another set of content appears here.")
        st.code("print('Hello from Option C!')", language="python")
