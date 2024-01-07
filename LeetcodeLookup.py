import requests
import streamlit as st
from datetime import date
from requester import LeetcodeRequester


st.header("Leetcode Lookup 🚀")


# Get the username from the text input field
username = st.text_input("Enter the **LeetCode Username** 🤖")

# Button to submit the username
if st.button("Submit"):
    if username:
        # Create an instance of LeetcodeRequester
        leetcode_requester = LeetcodeRequester()
        leetcode_requester.ask(username)
        st.markdown("---")
        st.write(leetcode_requester.output())
        #st.markdown("---")
        # st.write(leetcode_requester.generate_horizontal_bar_chart())
        # st.write(leetcode_requester.generate_pie_chart())
        #st.write(leetcode_requester.generate_donut_chart())
        # st.write(leetcode_requester.generate_word_cloud())
        st.write(leetcode_requester.generate_scatter_plot())
    else:
        st.error("Enter a username")





#st.write("A FUN PROJECT OF MINE")