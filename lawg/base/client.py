from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod
from lawg.schemas import (
    APISuccessSchema,
    ProjectBodySchema,
    ProjectSchema,
    FeedCreateBodySchema,
    FeedPatchBodySchema,
    FeedSchema,
)

from lawg.typings import STR_DICT, UNDEFINED, P, F, L

if t.TYPE_CHECKING:
    from lawg.base.rest import BaseRest
    from lawg.typings import Undefined


class BaseClient(ABC, t.Generic[P, F, L]):
    """
    The base client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: BaseRest

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def project(self, project_namespace: str) -> P:
        """
        Get a project.

        Args:
            project_namespace (str): namespace of project.
        """

    @abstractmethod
    def feed(self, project_namespace: str, feed_name: str) -> F:
        """
        Get a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
        """

    # --- PROJECTS --- #

    @abstractmethod
    def create_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> P:
        """
        Create a project.

        Args:
            name (str): name of project.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def fetch_project(
        self,
        project_namespace: str,
    ) -> P:
        """
        Fetch a project.

        Args:
            namespace (str): namespace of log.
        """

    @abstractmethod
    def edit_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> P:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def delete_project(
        self,
        project_namespace: str,
    ) -> P:
        """
        Delete a project.

        Args:
            namespace (str): namespace of project.
        """

    patch_project = edit_project
    get_project = fetch_project

    # --- FEEDS --- #

    @abstractmethod
    def create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
    ) -> F:
        """
        Create a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of the feed.
            description (str | None, optional): description of feed. Defaults to None.
        """

    @abstractmethod
    def edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> F:
        """
        Edit a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed
            name (str | None, optional): new name of feed. Defaults to keeping the existing value.
            description (str | None, optional): new description of feed. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of feed. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_feed(
        self,
        project_namespace: str,
        feed_name: str,
    ) -> F:
        """
        Delete a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
        """

    patch_feed = edit_feed

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
            title (str | None, optional): new title of log. Defaults to keeping the existing value.
            description (str | None, optional): new description of log. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of log. Defaults to keeping the existing value.
            color (str | None, optional): new color of log. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
    ) -> L:
        """
        Delete a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log

    # --- FEEDS --- #

    def _validate_project_response(self, response_data: STR_DICT) -> STR_DICT:
        resp_schema = APISuccessSchema()
        resp_data: STR_DICT = resp_schema.load(response_data)  # type: ignore

        project_schema = ProjectSchema()
        project_data: STR_DICT = project_schema.load(resp_data["data"])  # type: ignore

        return project_data

    def _validate_create_request(self, project_namespace: str, project_name: str) -> STR_DICT:
        req_schema = ProjectBodySchema()
        req_data: STR_DICT = req_schema.load({"name": project_name, "namespace": project_namespace})  # type: ignore
        return req_data

    def _validate_fetch_request(self, project_namespace: str) -> None:
        req_schema = ProjectGetSchema()
        req_schema.load({"namespace": project_namespace})

    _validate_edit_request = _validate_create_request
    _validate_delete_request = _validate_fetch_request

    def _validate_feed_response(self, response_data: STR_DICT) -> STR_DICT:
        resp_schema = APISuccessSchema()
        resp_data: STR_DICT = resp_schema.load(response_data)  # type: ignore

        feed_schema = FeedSchema()
        feed_data: STR_DICT = feed_schema.load(resp_data["data"])  # type: ignore
        return feed_data

    def _validate_feed_create_request(
        self, project_namespace: str, feed_name: str, description: str | None = None, emoji: str | None = None
    ) -> None:
        req_schema = FeedCreateBodySchema()
        req_schema.load(
            {
                "namespace": project_namespace,
                "name": feed_name,
                "description": description,
                "emoji": emoji,
            }
        )
        return None

    def _validate_feed_edit_request(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> None:
        req_schema = FeedPatchBodySchema()
        req_schema.load(
            {
                "namespace": project_namespace,
                "name": feed_name,
                "new_name": name,
                "description": description,
                "emoji": emoji,
            }
        )

    def _validate_feed_delete_request(self, project_namespace: str, feed_name: str) -> None:
        req_schema = FeedDeleteSchema()
        req_schema.load({"namespace": project_namespace, "name": feed_name})
