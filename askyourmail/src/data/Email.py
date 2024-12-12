import datetime
from askyourmail.src.util.Constants import *


class Email:
    def __init__(self, thread_id, subject, from_, to, body, timestamp):
        """
        Initialize an Email instance.
        :param thread_id: Identifier for the email thread.
        :param subject: Subject of the email.
        :param timestamp: Date and time the email was sent/receive.
        :param from: Sender of the email.
        :param to: Recipient(s) of the email.
        :param body: Body of the email.
        """
        self.thread_id = thread_id
        self.subject = subject
        if(COLLECTION_NAME=="emails2"):
            self.timestamp = int(timestamp)
            self.date = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timestamp = timestamp
            self.date = self.timestamp
        self.from_ = from_
        self.to = to
        self.body = body

    def __repr__(self):
        """
        Representation of the Email instance.
        """
        return (f"Email(thread_id='{self.thread_id}', subject='{self.subject}', timestamp='{self.timestamp}', "
                f"from_='{self.from_}', to='{self.to}', body='{self.body}')")

    def to_dict(self):
        """
        Convert the Email instance to a dictionary for serialization.
        """
        return {
            "thread_id": str(self.thread_id),
            "subject": self.subject,
            "timestamp": self.timestamp,
            "date" : self.date,
            "from": self.from_,
            "to": self.to,
            "body": self.body
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create an Email instance from a dictionary.
        :param data: Dictionary containing email data.
        :return: Email instance.
        """
        return cls(
            thread_id=data.get("thread_id"),
            subject=data.get("subject"),
            from_=data.get("from"),
            to=data.get("to"),
            body=data.get("body"),
            timestamp=data.get("timestamp")
        )

    def to_string(self):
        """
        Convert the Email instance to a string representation.
        """
        return (f"Thread ID: {self.thread_id}\n"
                f"Subject: {self.subject}\n"
                f"Timestamp: {self.timestamp}\n"
                f"Date: {self.date}\n"
                f"From: {self.from_}\n"
                f"To: {self.to}\n"
                f"Body: {self.body}")