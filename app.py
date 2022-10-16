import streamlit as st
import time

import prepocessor, helper
import matplotlib.pyplot as plt

import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer \n Hey eveyone it's me Deepak")

# st.warning("""Idhar kya dekh raha hai ?? 👀\nFile upload karke "Show analysis" pe click kiya ??""")

text = """Sabar karo 🤚 process ho raha hai ........."""
t = st.empty()
for i in range(len(text) + 1):
    t.markdown("## %s..." % text[0:i])
    time.sleep(0.1)
text = """"""



# Uploading of file ==> https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    st.balloons()
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Convert above byte stream into string (utf-8 String)
    data = bytes_data.decode("utf-8")

    # st.text(data)                         #display uploaded file's data on stream or right of screen
    # We have to firsly preprocess the data
    df = prepocessor.preprocess(data)

    # # Display data frames
    # st.dataframe(df)



    # Now we have to create a dropdown to choose between various users

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    # group_notification is not a user, so simply remove it
    user_list.remove('group_notification')
    # Sort user list in ascending order
    user_list.sort()
    # If we want to do analysis(group level analysis) on overall users of the group ==> Insert "Overall" at 0th position :
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to : ", user_list)




    # Add a button for showing analysis
    if st.sidebar.button("Show analysis"):

        # Progress Bar
        st.balloons()
        # st.snow()

        st.title("👇👇👇 Ye raha aapka result tadaa 👇👇👇")

        # Fetch stats from "helper" file
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        # Show statistics
        # Create 4 columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)












        # Timeline

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)








        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='gold')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)








        # activity map
        st.title('Activity Map ⤵')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)








        # Activity heatmap
        st.title("Weekly Activity Heat Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)







        # Finding the busiest/active users in the group (Group Level) :
        if selected_user == "Overall":
            st.title("Most active user 👇")

            # Fetch most busy users from helper.py
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="green")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)









            # Wordcoud
            st.title("Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)                                      # imshow ====> Image Show
            st.pyplot(fig)

            # # WordCloud
            # st.title("Wordcloud")
            # df_wc = helper.create_wordcloud(selected_user, df)
            # fig, ax = plt.subplots()
            # ax.imshow(df_wc)
            # st.pyplot(fig)








            # Most Common Words
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title("Most common words")
            st.pyplot(fig)

            # st.dataframe(most_common_df)













            # Emoji Analysis
            emoji_df = helper.emoji_helper(selected_user, df)
            st.title("Emoji analsis")

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:

                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

                st.pyplot(fig)