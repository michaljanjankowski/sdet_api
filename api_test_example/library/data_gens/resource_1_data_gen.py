from api_test_example.models import Resource1PostRequest


class Resource1DataGen:
    def create_data(self, field1: str, field2: str) -> Resource1PostRequest:
        return Resource1PostRequest(field1=field1, field2=field2)
