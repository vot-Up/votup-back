from typing import Protocol

class FileStoragePort(Protocol):
    def upload(self, file: bytes, filename: str) -> str:
        ...

    def delete(self, file_url: str) -> None:
        ...