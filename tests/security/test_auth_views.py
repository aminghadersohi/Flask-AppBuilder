from types import SimpleNamespace

import pytest
from flask import Flask, g

from flask_appbuilder.security.views import (
    AuthDBView,
    AuthLDAPView,
    AuthOAuthView,
    AuthRemoteUserView,
    AuthSAMLView,
)


@pytest.mark.parametrize(
    "view_class",
    [AuthDBView, AuthLDAPView, AuthOAuthView, AuthSAMLView, AuthRemoteUserView],
)
@pytest.mark.parametrize(
    ("next_url", "expected"),
    [("/users/list/", "/users/list/"), ("https://example.com/", "/")],
)
def test_authenticated_login_uses_safe_next_url(view_class, next_url, expected):
    """Every browser authentication type handles an existing session alike."""
    app = Flask(__name__)
    appbuilder = SimpleNamespace(
        get_url_for_index="/",
        sm=SimpleNamespace(auth_remote_user_env_var="REMOTE_USER"),
    )
    app.appbuilder = appbuilder
    view = view_class()
    view.appbuilder = appbuilder

    with app.test_request_context("/login/", query_string={"next": next_url}):
        g.user = SimpleNamespace(is_authenticated=True)
        response = view.login()

    assert response.status_code == 302
    assert response.location == expected
