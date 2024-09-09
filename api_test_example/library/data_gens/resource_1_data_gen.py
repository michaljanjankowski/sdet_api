from product_source_code import Resource1PostRequest


class Resource1DataGen():
    def create_data(self, **kwargs) -> Resource1PostRequest:
        return Resource1PostRequest1(field1 = kwargs.get("field1"),
                                     field2 = kwargs.get("field2"))
