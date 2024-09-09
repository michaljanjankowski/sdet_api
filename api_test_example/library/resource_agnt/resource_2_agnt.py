from api_test_example.library.resource_agnt.base import ResourceInfoBase, AgentBase



class Resource2_Info(ResourceInfoBase):
    name: str

    def identifier(self) -> str:
        return self.name


class Resource2Agnt(AgentBase[Resource2_Info]):  # pylint: disable=too-many-public-methods
    RESOURCE_NAME = "resource2"
    RESOURCE_TYPE = Resource2_Info