from django_filters import filterset

from account import choices, models


class FilterBase(filterset.FilterSet):
    id = filterset.CharFilter(field_name="id", lookup_expr=choices.EXACT)
    created_at = filterset.DateTimeFilter(field_name="created_at", lookup_expr=choices.EXACT)
    modified_at = filterset.DateTimeFilter(field_name="modified_at", lookup_expr=choices.EXACT)
    active = filterset.BooleanFilter(field_name="active", lookup_expr=choices.EXACT)


class UserFilter(FilterBase):
    name = filterset.CharFilter(field_name="name", lookup_expr=choices.LIKE)
    password = filterset.CharFilter(field_name="password", lookup_expr=choices.EXACT)
    cellphone = filterset.CharFilter(field_name="cellphone", lookup_expr=choices.EXACT)
    email = filterset.CharFilter(field_name="email", lookup_expr=choices.IEXACT)
    is_active = filterset.BooleanFilter(field_name="is_active", lookup_expr=choices.EXACT)

    class Meta:
        model = models.User
        fields = ["id", "created_at", "modified_at", "is_active", "name", "password", "email"]
