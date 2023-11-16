import matplotlib.pyplot as plt
import streamlit as st
import Preprocessor
import helper
import seaborn as sns

st.success("# Analyze Your WhatsApp Chats")
st.sidebar.title("WhatsApp Chat Analyzer")
# Uploding files using file streamlit uploader

uploaded_file=st.sidebar.file_uploader("choose a file")
st.sidebar.info("###### Uploade Your WhatsApp Chats Here")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()

    data=bytes_data.decode("utf-8")
    df=Preprocessor.preprocess(data)

# decode the file using utf-8 and turn it into variable name
# as data. then call the preprocessor function and pass the
# data that function preprocess the data

# here, the text file is decoded and get in the variable name
# as data and here preprocessor----> file name
# and preprocess---->function where data is ready and clean

    #st.dataframe(df) # gives dataset on streamlit display.

    ## ** Fetch Unique Users
    user_list=df["user"].unique().tolist()#All unique user are in list

    user_list.remove("group_notification")
    # Here remove group notification from users list

    user_list.sort()
    user_list.insert(0,"Overall")
    # we sort the user name ascending order and inserting a
    # name overall for analysis of all the data

    selected_user=st.sidebar.selectbox("Show analysis WRT ",user_list)
    # here all uniques name that stored in list are show here and
    # also show the variable overall for all the analysis.

    if st.sidebar.button("Show Analysis"):



        ## ** Satastic area

        no_messages,words,no_media_files,no_links=helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)#multi-columns at once


        with col1:
            st.header("Total Messages")
            st.title(no_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(no_media_files)

        with col4:
            st.header("Links Shared")
            st.title(no_links)

        ## ** Monthly Timeline
        #----------------------
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"],color="purple")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        ## ** Daily Timeline
        #---------------------
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["message"], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)



        ## ** Activity Map
        # ------------------

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busiest Day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values,color="lime")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)



        ## ** HeatMap
        #------------

        st.title("Weekly Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)

        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)









        ## ** Most Busiest person
        #-----------------------

        if selected_user == "Overall":
            st.title("Most Busy User")

            x,new_df=helper.most_busy_users(df)

            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="violet")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        ## ** WordCloud
        #----------------

        st.title("Word-Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        ## ** Most common Words
        #-----------------------

        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax=plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1],color="maroon")
        plt.xticks(rotation="vertical")

        st.title("Most Common Words")
        st.pyplot(fig)


        ## ** Emoji Analysis
        #--------------------

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        st.success("# Complete Analysis  !! Thank-You !!")





