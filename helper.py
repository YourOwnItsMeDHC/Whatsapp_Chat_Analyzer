# These file will contain functions

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extractor = URLExtract()

# def fetch_stats(selected_user, df):
    # if selected_user == 'Overall':
    #     # We want to do group level analysis
    #
    #     # 1. Fetch number of messages
    #     num_messages = df.shape[0]         # 0th index shows number of messages, shape returns number of messages
    #     # 2. Fetch number of words
    #     word = []
    #     for message in df['message']:
    #         word.extend(message.split())
    #
    #     return num_messages, len(word)
    #
    # else:
    #
    #     # 1. Fetch number of messages
    #     # Fetch all the rows, wherever that paricular user is
    #     new_df = df[df['user'] == selected_user]           # Here, we are doing masking
    #     num_messages = new_df.shape[0]
    #
    #     # 2. Fetch number of words
    #     word = []
    #     for message in new_df['message']:
    #         word.extend(message.split())
    #
    #     return num_messages, len(word)

    # Same code as above, but shorter one :
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. Fetch number of messages
    num_messages = df.shape[0]

    # 2. Fetch number of words
    word = []
    for message in df['message']:
        word.extend(message.split())

    # 3. Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. Fetch number of links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(word), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()

    # Percentage of messages of each user :
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})

    return x, df


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')  # 'r' =====> Read Mode
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove "group_notification" messages
    # remove media omitted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # Create object of wordcloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    temp['message'] = temp['message'].apply(remove_stop_words)

    # Generate wordcloud image, wordcloud will get create from "message" column
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc






def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')  # 'r' =====> Read Mode
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove "group_notification" messages
    # remove media omitted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))  # Most frequent used 20 words
    return most_common_df









def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df









def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline










def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline







def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()









def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()













def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


