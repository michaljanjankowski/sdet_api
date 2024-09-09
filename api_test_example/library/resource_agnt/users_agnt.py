from api_test_example.library.resource_agnt.base import ResourceInfoBase, AgentBase


class User_Info(ResourceInfoBase):
    pass


class UsersAgnt(AgentBase[User_Info]):
    pass
