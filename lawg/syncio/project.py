from __future__ import annotations

import typing as t

from lawg.base.project import BaseProject
from lawg.exceptions import LawgAlreadyDeleted
from lawg.syncio.feed_manager import FeedManager
from lawg.syncio.log_manager import LogManager
from lawg.syncio.insight_manager import InsightManager

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.feed import Feed
    from lawg.syncio.log import Log
    from lawg.syncio.member import Member


class Project(BaseProject["Client", "Feed", "Log", "Member"]):
    # --- MANAGERS --- #

    def feed(self, name: str):
        return FeedManager(client=self.client, project_namespace=self.namespace, feed_name=name)

    def log(self, feed_name: str, log_id: str):
        return LogManager(client=self.client, project_namespace=self.namespace, feed_name=feed_name, id=log_id)

    def insight(self):
        return InsightManager(client=self.client, project_namespace=self.namespace)

    # --- PROJECT --- #

    def edit(self, name: str):
        self.client.rest._edit_project(project_namespace=self.namespace, project_name=name)
        self.name = name

    def delete(self):
        if self.is_deleted:
            raise LawgAlreadyDeleted("project")

        self.client.rest._delete_project(project_namespace=self.namespace)
        self.is_deleted = True
