class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_initials: str
    client_name: str
    epic_name: str
    start_time: str
    end_time: str
    month: Optional[int]
    year: Optional[int]


input_timelog = timelog
input_timelog.user_initials = "ac"  # nie tak
new_timelog = TimeLog(
    id=input_timelog.id, user_initials="ac", client_name=input_timelog.client_name
)
