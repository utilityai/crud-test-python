import logging
from dataclasses import dataclass

import requests
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TodoRecord:
    def __init__(self, content: str, is_complete: bool):
        self.content = content
        self.is_complete = is_complete


# HTTP client for interacting with the to-do server
class TodoClient:
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url

    # Get a to-do record by its ID
    def get(self, id: int) -> Optional[TodoRecord]:
        response = requests.get(f"{self.server_url}/{id}")

        if response.status_code == 200:
            json = response.json()
            return TodoRecord(
                content=json["content"],
                is_complete=json["is_complete"]
            )
        elif response.status_code == 404:
            return None
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")

    # Create a to-do record
    def create(self, todo_record: TodoRecord) -> int:
        response = requests.post(self.server_url, json=todo_record.dict())

        if response.status_code == 200:
            return response.json()["id"]
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")

    # Delete a to-do record
    def delete(self, id: int) -> bool:
        response = requests.delete(f"{self.server_url}/{id}")

        return response.status_code == 200


def main():
    # create the client
    client = TodoClient()

    # check does not exist for -1
    non_existing_id = -1
    does_not_exist_yet = client.get(non_existing_id)
    if does_not_exist_yet is not None:
        logger.error(f"{non_existing_id} should never exist!")
    else:
        logger.info(f"As expected, received null from server for {non_existing_id}")

    # create a new to-do
    todo_record = TodoRecord("complete a coding test", False)
    new_id = client.create(todo_record)
    logger.info(f"Created to-do {new_id}")

    # fetch the new to-do
    fetched = client.get(new_id)

    # check the fetched to-do matches the to-do we created
    if fetched is None:
        logger.error(f"{new_id} is null despite us just creating it")
    elif fetched != todo_record:
        logger.error(f"To-do {new_id} does not match what we inserted")
    else:
        logger.info(f"Created and fetched to-do {new_id} as expected")

    # delete the to-do
    success = client.delete(new_id)
    if not success:
        logger.error(f"Delete failed for id {new_id}")
    else:
        logger.info(f"Delete success for id {new_id}")

    # check we can no longer fetch the deleted to-do
    deleted_record = client.get(new_id)

    if deleted_record is not None:
        logger.error(f"Delete failed for id {new_id} - to-do still exists!")
    else:
        logger.info(f"As expected, was unable to get to-do {new_id} after deletion")


if __name__ == '__main__':
    main()
