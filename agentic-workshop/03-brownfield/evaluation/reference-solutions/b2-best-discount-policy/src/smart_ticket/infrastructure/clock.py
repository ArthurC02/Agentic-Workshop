from datetime import date, datetime, time, timezone, timedelta

class FixedClock:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.today = date(2030, 1, 14)

    def now(self) -> datetime:
        return datetime.combine(self.today, time(9), tzinfo=timezone(timedelta(hours=8)))
