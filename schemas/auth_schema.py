from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    name: str
    email: str
    
class UserDataPASS(UserData):
    hashed_password: str
    """
    UserDataPASS는 UserData 클래스를 상속받은 클래스입니다. 
    즉, UserDataPASS는 UserData에 있는 모든 필드를 포함하고, 
    추가적으로 hashed_password라는 필드를 더 포함합니다.
    """