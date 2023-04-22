import dataclasses

from common.util.util import bool_check


@dataclasses.dataclass
class User:
    id: int
    name: str
    auth_key: str


@dataclasses.dataclass
class RouterConfig:
    id: int
    slack_integration: bool = False
    rocket_integration: bool = False
    telegram_integration: bool = False
    slack_token: str = None
    telegram_token: str = None
    telegram_chat_id: str = None
    rocket_login: str = None
    rocket_password: str = None
    
    def __post_init__(self):
        if (
            (self.slack_integration and not self.slack_token) or
            (self.rocket_integration and not all([self.rocket_login, self.rocket_password])) or
            (self.telegram_integration and not all([self.telegram_token, self.telegram_chat_id]))
        ):
            raise Exception('Invalid integration config! Check values in db!')
        
