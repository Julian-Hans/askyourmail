class Conversation:
    def __init__(self, thread_id, emails=None):
        """
        Initialize a Conversation instance.
        :param thread_id: Identifier for the conversation thread.
        :param emails: List of Email objects belonging to the thread.
        """
        self.thread_id = thread_id
        self.emails = emails if emails else []

    def add_email(self, email):
        """
        Add an email to the conversation.
        :param email: Email object to add.
        """
        self.emails.append(email)

    def to_dict(self):
        """
        Convert the Conversation instance to a dictionary for serialization.
        """
        return {
            "thread_id": self.thread_id,
            "emails": [email.to_dict() for email in self.emails]
        }

    def __repr__(self):
        """
        Representation of the Conversation instance.
        """
        return f"Conversation(thread_id='{self.thread_id}', num_emails={len(self.emails)})"
