from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Social Media Sentiment Analyzer"
    admin_email: str = "patrickokoagwu@gmail.com"
    access_token_expire_minutes: int  = 30
    refresh_token_expire_minutes : int = 60*24*7
    algorithm: str = "HS256"
    jwt_secret_key: str = "NEA0wdX9H8bgYQEsHAWo0736XI4/D6O48USLrCApedt1XyEsAxF5e/e8Xf72a3kQf9FNtV8nMBTONTH2av5LhOju/0dcCvGVk4ketm8zjydH+tm1oNMVeXIn1vlW8DjzDmCHnfDiXtmzWzS25bLJKfxjBeCW8W6mEZ8ir+GIyC8tj0Z1bdR56j+kskscN7OuIMySa+4QFCXD6YzefmXAw8oOXfUuMqRvcS47bw=="
    jwt_refresh_secret_key: str = "DecA33ShZvcNXgfNfTFVTnD51KXD0y+CckwdenxahpGp3+pTV3rue3V2tPXcUEgNNfbUyUCtHdha8CCiQlc/ooWg0K/cNnD/etmDvKurq9+LBL2UHlANUFH26/yNlqJSfBu94PcfuX97uMnDvoKmA68HAhCUWULRlHm8OB3Fw7Kq9Rx8FBH3aA2mNURd735gjHB3A3/u4qGfh6QBBbt9qSsPVtwx53wbK0TyIw=="



settings = Settings()