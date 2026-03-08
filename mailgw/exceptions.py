class MailGWError(Exception):
    pass


class AuthenticationError(MailGWError):
    pass


class APIError(MailGWError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API error {status_code}: {message}")
