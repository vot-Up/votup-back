import importlib
from copy import deepcopy


class ViewSetExpandMixin:
    def make_queryset_expandable(self, request):
        expand_fields = request.query_params.get("expand", None)
        if not expand_fields:
            return

        serializer_class = deepcopy(self.serializer_class)

        if "~all" in expand_fields or "*" in expand_fields:
            expand_fields = ",".join(serializer_class.expandable_fields)

        for expand in expand_fields.split(","):
            self.queryset = self._apply_expansion(serializer_class, expand.strip())

    def _apply_expansion(self, serializer_class, expand):
        previous_source = ""
        previous_field = None
        found_many = False
        queryset = self.queryset

        for nested_field in expand.split("."):
            field = nested_field.strip()

            settings = self._get_field_settings(serializer_class, previous_field, field)
            source = settings.get("source", field)
            many = settings.get("many", False)

            related_path = f"{previous_source}{source}" if previous_source else source

            if many or found_many:
                queryset = queryset.prefetch_related(related_path)
            else:
                queryset = queryset.select_related(related_path)

            previous_source += f"{source}__"
            previous_field = field
            serializer_class = self._get_serializer_class(serializer_class, previous_field)

            if not found_many:
                found_many = many

        return queryset

    def _get_field_settings(self, serializer_class, previous_field, field):
        if not previous_field:
            return serializer_class.expandable_fields[field][1]
        serializer_path = serializer_class.expandable_fields[previous_field][0]
        pieces = serializer_path.split(".")
        class_name = pieces.pop()

        if pieces[-1] != "serializers":
            pieces.append("serializers")

        module = importlib.import_module(".".join(pieces))
        nested_serializer_class = getattr(module, class_name)
        return nested_serializer_class.expandable_fields[field][1]

    def _get_serializer_class(self, serializer_class, previous_field):
        serializer_path = serializer_class.expandable_fields[previous_field][0]
        pieces = serializer_path.split(".")
        class_name = pieces.pop()

        if pieces[-1] != "serializers":
            pieces.append("serializers")

        module = importlib.import_module(".".join(pieces))
        return getattr(module, class_name)
