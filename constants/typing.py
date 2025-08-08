from typing import *  # noqa: F403

from django.db.models import Model, QuerySet

ModelType = TypeVar("ModelType", bound=Model)  # noqa: F405

QuerySetType = QuerySet[ModelType]

CompanyModelQuery = TypeVar("CompanyModelQuery", bound=Model)  # noqa: F405
CompanyProfileType = TypeVar("CompanyProfile", bound=Model)  # noqa: F405
CompanyUserType = TypeVar("CompanyUser", bound=Model)  # noqa: F405

UserType = TypeVar("User", bound=Model)  # noqa: F405
