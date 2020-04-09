from cgi import parse_header
from datetime import datetime, timedelta
from urllib.parse import quote, unquote, urljoin

import requests


class BakaAPIException(Exception):
    pass


class InvalidCredentials(BakaAPIException):
    pass


class InvalidResponse(BakaAPIException):
    pass


class BakapiUser:
    token_valid_until = None
    refresh_token = None
    access_token = None
    url = None
    username = None

    def __init__(self, *args, url, username, password, **kwargs):
        self.url = url
        self.username = username

        self.create_token(password)
        super().__init__(*args, **kwargs)

    def authenticate(self, data):
        """Takes authentication data, sends request and stores results"""

        t = datetime.now()
        r = requests.post(urljoin(self.url, "api/login"), data=data)
        if not r.headers["Content-Type"].lower().startswith("application/json"):
            raise InvalidResponse

        d = r.json()

        if "error" in d:
            e = d["error"]
            if e == "invalid_grant":
                raise InvalidCredentials
            else:
                raise BakaAPIException

        self.access_token = d["access_token"]
        self.refresh_token = d["refresh_token"]
        self.token_valid_until = t + timedelta(seconds=d["expires_in"] - 10)

    def create_token(self, password):
        """Authenticates via username and password"""

        self.authenticate(
            {
                "client_id": "ANDR",
                "grant_type": "password",
                "username": self.username,
                "password": password,
            }
        )

    def use_refresh_token(self):
        """Refreshes the authentication using the refresh token"""

        return self.authenticate(
            {
                "client_id": "ANDR",
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }
        )

    def send_request(self, endpoint, method="GET", **kwargs):
        """Checks token validity and sends the request"""

        if self.token_valid_until < datetime.now():
            self.use_refresh_token()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = "Bearer " + self.access_token

        r = requests.request(
            method,
            urljoin(self.url, endpoint),
            headers=headers,
            **kwargs
        )
        return r

    def query_api(self, endpoint, method="GET", **kwargs):
        """Processes the JSON response"""

        r = self.send_request(endpoint, method, **kwargs)

        if not r.headers["Content-Type"].lower().startswith("application/json"):
            raise InvalidResponse

        d = r.json()

        if "error" in d:
            e = d["error"]
            if e == "invalid_grant":
                raise InvalidCredentials
            else:
                raise BakaAPIException
        return d

    def get_user_info(self):
        return self.query_api("api/3/user")

    def get_homework(self):
        return self.query_api("api/3/homeworks")

    def get_received_komens_messages(self):
        return self.query_api("api/3/komens/messages/received", method="POST")

    def download_attachment(self, attachment_id):
        """Downloads the attachment with given id and returns (filename, readable stream)"""
        r = self.send_request(
            "api/3/komens/attachment/" + quote(attachment_id), stream=True
        )

        if r.headers["Content-Type"] != "application/octet-stream":
            raise InvalidResponse

        filename = unquote(
            parse_header(r.headers["Content-Disposition"])[1]["filename*"][7:]
        )
        return filename, r.raw
