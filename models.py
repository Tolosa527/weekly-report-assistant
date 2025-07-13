from pydantic import BaseModel

class Params(BaseModel):
    start_date: str
    end_date: str
    username: str

    def dict(self):
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "username": self.username
        }