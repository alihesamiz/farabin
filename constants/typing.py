from typing import TypeVar

from django.db.models import Model, QuerySet

# Define a generic ModelType for type hinting
ModelType = TypeVar("ModelType", bound=Model)

# Type for querysets of any model (e.g. CompanySWOTOption, SWOTOption, etc.)
QuerySetType = QuerySet[ModelType]

# Type hint for a function that takes a model and a company and returns a queryset of that model
CompanyModelQuery = TypeVar("CompanyModelQuery", bound=Model)
