import json
from typing import Any, Mapping, Optional

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """Custom method."""

    charset = "utf-8"

    def render(
        self,
        data: dict[str, Any],
        media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> str:
        """Return a well formatted user jSON."""
        errors = data.get("errors", None)
        token = data.get("token", None)
        if errors is not None:
            return json.dumps({"errors": errors})

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
