import streamlit as st
import time
import prepocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer \n Hey everyone your it's me Deepak 😊")

uploaded_file = st.sidebar.file_uploader("Choose a file")

# Initial message if no file is uploaded
if not uploaded_file:
    text = "Sabar karo 🤚 process ho raha hai ............"
    t = st.empty()
    for i in range(len(text) + 1):
        t.markdown("## %s..." % text[0:i])
        time.sleep(0.1)
    st.stop()

if uploaded_file:
    st.balloons()
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = prepocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to: ", user_list)

    if not st.sidebar.button("Show analysis"):
        st.title("""Idhar kya dekh raha hai ?? 👀\nFile upload karke "Show analysis" pe click kiya ??""")
        st.stop()

    
       text = "Sabar karo 🤚 process ho raha hai ............"
       t = st.empty()

       display_duration = 5
       start_time = time.time()

      for i in range(len(text) + 1):
         t.markdown("## %s..." % text[0:i])
         time.sleep(0.1)

    if time.time() - start_time > display_duration:
        break
    
    time.sleep(0.1)

    # text = "Data processed Bro 💪"
    # t = st.empty()

    # display_duration = 5
    # start_time = time.time()

    # for i in range(len(text) + 1):
    #     t.markdown("## %s..." % text[0:i])
    #     time.sleep(0.1)

    # # if time.time() - start_time > display_duration:
    # #     break
    
    # time.sleep(0.1)
    
    t.empty()
    
    # Analysis code starts here
    st.balloons()
    st.title("👇 Ye raha aapka result tadaa 👇")
        
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    st.title("Top Statistics")
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

    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='gold')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

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

    st.title("Weekly Activity Heat Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)

    # Debugging: Print heatmap data
    st.write("Heatmap Data:", user_heatmap)

    # Check for NaN values
    if user_heatmap.isnull().values.all():
        st.error("Heatmap data contains all NaN values. Please check the data processing steps.")
    else:
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, annot=True, fmt="d", cmap="YlGnBu")
        st.pyplot(fig)

    if selected_user == "Overall":
        st.title("Most active user 👇")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most common words")
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
