from typing import Generator, Tuple
from unittest.mock import MagicMock, patch

import pytest

from src.services.ingestion.mongo_repository import MongoRepository


@pytest.fixture
def mock_mongo_repo() -> Generator[Tuple[MongoRepository, MagicMock], None, None]:
    with patch(
        "src.services.ingestion.mongo_repository.DatabaseMongo"
    ) as MockDatabaseMongo:
        mock_db = MockDatabaseMongo.return_value
        mock_collection = MagicMock()
        mock_db.get_collection.return_value = mock_collection
        repo = MongoRepository()
        repo._collection = mock_collection
        yield repo, mock_collection


def test_insert_data(mock_mongo_repo: Tuple[MongoRepository, MagicMock]) -> None:
    repo, mock_collection = mock_mongo_repo
    data = {"key": "value"}
    repo.insert_data(data)
    mock_collection.insert_one.assert_called_once_with(data)


def test_get_all_data(mock_mongo_repo: Tuple[MongoRepository, MagicMock]) -> None:
    repo, mock_collection = mock_mongo_repo
    mock_collection.find.return_value = [{"a": 1}, {"b": 2}]
    result = repo.get_all_data()
    assert result == [{"a": 1}, {"b": 2}]
    mock_collection.find.assert_called_once()


def test_remove_all_data(mock_mongo_repo: Tuple[MongoRepository, MagicMock]) -> None:
    repo, mock_collection = mock_mongo_repo
    repo.remove_all_data()
    mock_collection.delete_many.assert_called_once_with({})
