from __future__ import annotations

import typing as t

import httpx

from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema, Undefined

if t.TYPE_CHECKING:
    from marshmallow import Schema
    from lawg.syncio.client import Client


from lawg.schemas import (
    FeedCreateBodySchema,
    FeedCreateSlugSchema,
    FeedDeleteSlugSchema,
    FeedPatchBodySchema,
    FeedPatchSlugSchema,
    InsightCreateBodySchema,
    InsightCreateSlugSchema,
    InsightGetMultipleBodySchema,
    InsightGetSlugSchema,
    InsightPatchBodySchema,
    InsightPatchSlugSchema,
    InsightValueSchema,
    LogCreateBodySchema,
    LogCreateSlugSchema,
    LogDeleteSlugSchema,
    LogGetMultipleBodySchema,
    LogGetMultipleSlugSchema,
    LogGetSlugSchema,
    LogPatchBodySchema,
    LogPatchSlugSchema,
    ProjectDeleteSlugSchema,
    ProjectGetSlugSchema,
    ProjectPatchBodySchema,
    ProjectPatchSlugSchema,
    ProjectSchema,
    FeedSchema,
    LogSchema,
    InsightSchema,
    ProjectCreateBodySchema,
)


class Rest(BaseRest["Client", httpx.Client]):
    """The syncio rest manager."""

    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.http_client = httpx.Client()
        self.http_client.headers.update(self.headers)

    def request(
        self,
        *,
        url: str,
        method: str,
        body_with_schema: DataWithSchema | None = None,
        slugs_with_schema: DataWithSchema | None = None,
        response_schema: Schema | None = None,
    ) -> STR_DICT:
        url, body_dict = self.prepare_request(url, body_with_schema, slugs_with_schema)

        resp = self.http_client.request(method=method, url=url, json=body_dict)

        return self.prepare_response(resp, response_schema=response_schema)

    # --- PROJECTS --- #

    def create_project(self, project: str, project_name: str):
        body = {
            "namespace": project,
            "name": project_name,
        }
        project_data = self.request(
            url=self.API_CREATE_PROJECT,
            method="POST",
            body_with_schema=DataWithSchema(body, ProjectCreateBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def fetch_project(self, project: str):
        slugs = {
            "namespace": project,
        }
        project_data = self.request(
            url=self.API_GET_PROJECT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, ProjectGetSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def edit_project(self, project: str, project_name: str):
        slugs = {
            "namespace": project,
        }
        body = {
            "name": project_name,
        }
        project_data = self.request(
            url=self.API_EDIT_PROJECT,
            method="PATCH",
            slugs_with_schema=DataWithSchema(slugs, ProjectPatchSlugSchema()),
            body_with_schema=DataWithSchema(body, ProjectPatchBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def delete_project(self, project: str) -> None:
        slugs = {
            "namespace": project,
        }
        self.request(
            url=self.API_DELETE_PROJECT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, ProjectDeleteSlugSchema()),
        )

    # --- FEEDS --- #

    def create_feed(
        self,
        project: str,
        feed: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
        }
        data = {
            "name": feed,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.request(
            url=self.API_CREATE_FEED,
            method="POST",
            body_with_schema=DataWithSchema(data, FeedCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedCreateSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    def edit_feed(
        self,
        project: str,
        feed: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "name": name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.request(
            url=self.API_EDIT_FEED,
            method="PATCH",
            body_with_schema=DataWithSchema(data, FeedPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedPatchSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    def delete_feed(self, project: str, feed: str) -> None:
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        self.request(
            url=self.API_DELETE_FEED,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, FeedDeleteSlugSchema()),
        )

    # --- LOGS --- #

    def create_log(
        self,
        project: str,
        feed: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = self.request(
            url=self.API_CREATE_LOG,
            method="POST",
            body_with_schema=DataWithSchema(data, LogCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogCreateSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def fetch_log(self, project: str, feed: str, log_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        log_data = self.request(
            url=self.API_GET_LOG,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, LogGetSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def fetch_logs(
        self,
        project: str,
        feed: str,
        limit: int | None = None,
        offset: int | None = None,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "limit": limit,
            "offset": offset,
        }
        logs_data: list[STR_DICT] = self.request(
            url=self.API_GET_LOGS,
            method="GET",
            body_with_schema=DataWithSchema(data, LogGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogGetMultipleSlugSchema()),
            response_schema=LogSchema(many=True),
        )  # type: ignore
        return logs_data

    def edit_log(
        self,
        project: str,
        feed: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = self.request(
            url=self.API_EDIT_LOG,
            method="PATCH",
            body_with_schema=DataWithSchema(data, LogPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogPatchSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def delete_log(self, project: str, feed: str, log_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        self.request(
            url=self.API_DELETE_LOG,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, LogDeleteSlugSchema()),
        )

    # --- INSIGHTS --- #

    def create_insight(
        self,
        project: str,
        title: str,
        description: str | None = None,
        value: float | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.request(
            url=self.API_CREATE_INSIGHT,
            method="POST",
            body_with_schema=DataWithSchema(data, InsightCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightCreateSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def fetch_insight(
        self,
        project: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        insight_data = self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightGetSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def fetch_insights(
        self,
        project: str,
    ):
        slugs = {
            "namespace": project,
        }
        insights_data: list[STR_DICT] = self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightGetMultipleBodySchema()),
            response_schema=InsightSchema(many=True),
        )  # type: ignore
        return insights_data

    def edit_insight(
        self,
        project: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: dict[str, float] | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.request(
            url=self.API_EDIT_INSIGHT,
            method="PATCH",
            body_with_schema=DataWithSchema(data, InsightPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightPatchSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def delete_insight(
        self,
        project: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        self.request(
            url=self.API_DELETE_INSIGHT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, InsightValueSchema()),
        )
