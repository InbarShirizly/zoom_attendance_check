import pandas as pd

class Session:
    """
    generate relevant chat for each session. message is marked as relevant if the zoom user wrote something that is
    part of the student list database, and it's unique to one that isn't already named
    """

    def __init__(self, students_df, df_session_chat, meta_data):
        """
        :param students_df: student list dataframe
        :param df_session_chat: chat of the relevant session (df)
        :param meta_data: meta data for the report (namedtuple)
        """
        self._first_message_time = df_session_chat["time"].sort_values().iloc[0]
        self._relevant_chat = self.get_relevant_chat_in_session(students_df, df_session_chat, meta_data)

    @ staticmethod
    def get_relevant_chat_in_session(df_students, df_chat, meta_data):
        """
        create chat dataframe with marking of relevant chat messages.
        :param df_chat: that table of the chat for the specific session
        :return: chat with marking of relevant chat messages (df)
        """
        final_df = None
        for mode in meta_data.filter_modes:
            # find messages that have exact information that is one of the cells in  the student list database
            merged_df = pd.merge(df_students, df_chat.reset_index(), left_on=mode, right_on="message", how="left")
            final_df = pd.concat([merged_df, final_df])

        final_df.sort_values(by="time", inplace=True)
        # get messages that are relevant - from all messages that have information - take the first one of each user
        df_participated = final_df.groupby("zoom_name").first().reset_index()
        df_participated["index"] = df_participated["index"].astype(int)
        # slice the df to contain only the columns that will be part of the chat table in the DB
        df_participated = df_participated.loc[:, ["id", "zoom_name", "time", "message", "index"]].set_index("index")

        # filter out zoom names in the chat that should not be included (visitor in the session or the teacher)
        filt = df_chat['zoom_name'].str.contains('|'.join(meta_data.zoom_names_to_ignore))
        df_relevant_chat = pd.merge(df_chat[~filt], df_participated, how="left")

        # find the messages that are relevant, change the id column to have id onlt for users that were mentioned
        df_relevant_chat["relevant"] = df_relevant_chat["id"].apply(lambda x: 1 if x == x else 0)
        df_relevant_chat["id"] = df_relevant_chat["id"].apply(lambda x: int(x) if x == x else -1)
        return df_relevant_chat

    def zoom_names_table(self, session_id):
        """
        create the zoom names table that will be inserted to the database
        :param session_id: number of referring session in the DB
        :return: df of relevant data of zoom names in the session
        """
        zoom_df = self._relevant_chat.loc[:, ["zoom_name", "id"]].rename(columns={"zoom_name": "name", "id": "student_id"})
        zoom_df['session_id'] = pd.Series([session_id] * zoom_df.shape[0])
        return zoom_df.sort_values(by="student_id", ascending=False).groupby("name").first().reset_index()

    def chat_table(self, zoom_df):
        """
        create the chat table that will be inserted to the database
        :param zoom_df: df from the database that have the zoom_named id that helps in the merging process
        :return: df of relevant chat data
        """
        relevant_chat = self._relevant_chat.drop(columns=["id"])
        chat_session_table = pd.merge(relevant_chat, zoom_df, left_on="zoom_name", right_on="name")
        return chat_session_table.drop(columns=["zoom_name", "name", "session_id", "student_id"]).rename(columns={"id": "zoom_names_id"})