import streamlit as st
from requester import LeetcodeRequester, InvalidUsernameError

st.header("VIEWCODE 🚀")
st.subheader("A Leetcode Statistic Tool")

# Get the username from the text input field
username = st.text_input("Enter the **LeetCode Username** 🤖")

# Button to submit the username
if st.button("Submit"):
    if username:
        # Create an instance of LeetcodeRequester
        leetcode_requester = LeetcodeRequester()
        
        try:
            # Make the request and get the metrics
            metrics = leetcode_requester.ask(username)

            # Display the metrics using the output method
            st.markdown("---")
            st.write(leetcode_requester.output())

            # # Uncomment the following lines if you want to display additional charts
            # st.markdown("---")
            # st.write(leetcode_requester.generate_horizontal_bar_chart())
            # st.write(leetcode_requester.generate_pie_chart())
            # st.write(leetcode_requester.generate_donut_chart())
            # # st.write(leetcode_requester.generate_word_cloud())
            st.write(leetcode_requester.generate_scatter_plot())
            # # st.write(leetcode_requester.generate_nightingale_rose_diagram())

        except InvalidUsernameError as e:
            st.error(str(e))
    else:
        st.error("Enter a username")
