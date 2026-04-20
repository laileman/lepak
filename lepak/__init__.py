from .client import LepakClient


def client(service_name: str, version: str, **kwargs) -> LepakClient:
    return LepakClient(service_name, version, **kwargs)
