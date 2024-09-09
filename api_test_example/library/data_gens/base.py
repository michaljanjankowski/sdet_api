from api_test_example.library.data_gens.resource_1_data_gen import Resource1DataGen
from api_test_example.library.data_gens.resource_2_data_gen import Resource2DataGen

class DataGen:
    def __init__(self) -> None:
        self.resource1gen = Resource1DataGen()
        self.resource2gen = Resource2DataGen()