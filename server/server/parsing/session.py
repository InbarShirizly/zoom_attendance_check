import pandas as pd

class Session:

    def __init__(self, students_df, df_session_chat, meta_data):

        self._first_message_time = df_session_chat["time"].sort_values().iloc[0]
        self._relevant_chat = self.get_participants_in_session(students_df, df_session_chat, meta_data)

    @ staticmethod
    def get_participants_in_session(df_students, df_chat, meta_data):
        """
        finds students that attendant to the session. runs over each mode which represent different way to declare that
        the student attendant (for example: phone number, ID). merges this data to the csv table with the zoom name that
        added it
        :param df_chat: that table of the chat for the specific session
        :return: df of the attendance in the session
        """
        final_df = None
        for mode in meta_data.filter_modes:
            merged_df = pd.merge(df_students, df_chat.reset_index(), left_on=mode, right_on="message", how="left")
            final_df = pd.concat([merged_df, final_df])

        final_df.sort_values(by="time", inplace=True)
        df_participated = final_df.groupby("zoom_name").first().reset_index()
        df_participated["index"] = df_participated["index"].astype(int)
        df_participated = df_participated.loc[:, ["id", "zoom_name", "time", "message", "index"]].set_index("index")

        filt = df_chat['zoom_name'].str.contains('|'.join(meta_data.zoom_names_to_ignore))
        df_relevant_chat = pd.merge(df_chat[~filt], df_participated, how="left")

        df_relevant_chat["relevant"] = df_relevant_chat["id"].apply(lambda x: 1 if x == x else 0)
        df_relevant_chat["id"] = df_relevant_chat["id"].apply(lambda x: int(x) if x == x else -1)
        return df_relevant_chat

    def zoom_names_table(self, session_id):
        zoom_df = self._relevant_chat.loc[:, ["zoom_name", "id"]].rename(columns={"zoom_name": "name", "id": "student_id"})
        zoom_df['session_id'] = pd.Series([session_id] * zoom_df.shape[0])
        return zoom_df.sort_values(by="student_id", ascending=False).groupby("name").first().reset_index()

    def chat_table(self, zoom_df):
        relevant_chat = self._relevant_chat.drop(columns=["id"])
        chat_session_table = pd.merge(relevant_chat, zoom_df, left_on="zoom_name", right_on="name")
        return chat_session_table.drop(columns=["zoom_name", "name", "session_id", "student_id"]).rename(columns={"id": "zoom_names_id"})