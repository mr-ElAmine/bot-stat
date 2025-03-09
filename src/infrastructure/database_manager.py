"""
src/infrastructure/database_manager.py

This module contains the DatabaseManager class, which manages the database connection and transactions using SQLAlchemy.
"""

import os
from typing import Any, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Result
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


class DatabaseManager:
    """
    This class manages the database connection and transactions using SQLAlchemy.
    """

    def __init__(self, database_url: str = "sqlite:///database.db") -> None:
        if database_url is None:
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            database_path = os.path.join(project_root, "database.db")
            database_url = f"sqlite:///{database_path}"

        self.engine = create_engine(database_url, echo=True)
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_database_connection(self) -> Session:
        """
        Retrieve a new database session.

        Returns:
            Session: A new SQLAlchemy session object.
        """
        return self.session_local()

    def create_to_database(self, instance: Any) -> None:
        """
        Save a new instance to the database.

        Parameters:
            instance: The SQLAlchemy model instance to be saved.

        Raises:
            Exception: If an error occurs during the commit, the session is rolled back and the exception is re-raised.
        """
        with self.get_database_connection() as session:
            try:
                session.add(instance)
                session.commit()
            except Exception:
                session.rollback()
                raise

    def update_to_database(self, instance: Any) -> None:
        """
        Update an existing instance in the database.

        Parameters:
            instance: The SQLAlchemy model instance to be updated.

        Raises:
            Exception: If an error occurs during the commit, the session is rolled back and the exception is re-raised.
        """
        with self.get_database_connection() as session:
            try:
                session.merge(instance)
                session.commit()
            except Exception:
                session.rollback()
                raise

    def delete_to_database(self, instance: Any) -> None:
        """
        Delete an instance from the database.

        Parameters:
            instance: The SQLAlchemy model instance to be deleted.

        Raises:
            Exception: If an error occurs during the commit, the session is rolled back and the exception is re-raised.
        """
        with self.get_database_connection() as session:
            try:
                session.delete(instance)
                session.commit()
            except Exception:
                session.rollback()
                raise

    def execute_raw_query(self, query: str, params: Optional[dict] = None) -> Result:
        """
        Execute a raw SQL query.

        Parameters:
            query (str): The raw SQL query.
            params (Optional[dict]): Parameters for the query. Defaults to None.

        Returns:
            Result: The result of the query execution.
        """
        with self.get_database_connection() as session:
            result: Result = session.execute(query, params or {})
            session.commit()
            return result
