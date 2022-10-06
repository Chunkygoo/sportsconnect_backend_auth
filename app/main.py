from typing import Any, Dict, List

import nest_asyncio
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.syncio import delete_user
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import (
    emailverification,
    session,
    thirdpartyemailpassword,
)
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface,
    APIOptions,
    SignUpPostOkResult,
)
from supertokens_python.recipe.emailpassword.types import FormField

from .config import settings


from supertokens_python.recipe.thirdpartyemailpassword import Google
from supertokens_python.recipe.thirdpartyemailpassword.interfaces import (
    ThirdPartyAPIOptions,
    EmailPasswordAPIOptions,
    ThirdPartySignInUpPostOkResult,
    EmailPasswordSignInPostOkResult,
    EmailPasswordSignUpPostOkResult,
)
from typing import Union
from supertokens_python.recipe.thirdparty.provider import Provider
from supertokens_python.recipe.emailpassword.types import FormField


def override_email_password_apis(original_implementation: APIInterface):
    original_sign_up_post = original_implementation.sign_up_post

    async def sign_up_post(
        form_fields: List[FormField],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ):
        # First we call the original implementation of signInPOST.
        response = await original_sign_up_post(form_fields, api_options, user_context)

        # Post sign up response, we check if it was successful
        if isinstance(response, SignUpPostOkResult):
            user_id = response.user.user_id
            email = response.user.email
            try:
                res = requests.post(
                    settings.api_data_url + "/auth/postsignup",
                    json={"id": user_id, "email": email},
                )
                if res.status_code != 201:  # API error
                    await delete_user(user_id)
                    return None
            except:  # Network error
                await delete_user(user_id)
                raise ValueError(
                    "An error occurred while posting the request to api_data_url"
                )
        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation


def override_thirdpartyemailpassword_apis(original_implementation: APIInterface):
    original_thirdparty_sign_in_up_post = (
        original_implementation.thirdparty_sign_in_up_post
    )
    original_emailpassword_sign_in_post = (
        original_implementation.emailpassword_sign_in_post
    )
    original_emailpassword_sign_up_post = (
        original_implementation.emailpassword_sign_up_post
    )

    async def thirdparty_sign_in_up_post(
        provider: Provider,
        code: str,
        redirect_uri: str,
        client_id: Union[str, None],
        auth_code_response: Union[Dict[str, Any], None],
        api_options: ThirdPartyAPIOptions,
        user_context: Dict[str, Any],
    ):
        # call the default behaviour as show below
        result = await original_thirdparty_sign_in_up_post(
            provider,
            code,
            redirect_uri,
            client_id,
            auth_code_response,
            api_options,
            user_context,
        )

        if isinstance(result, ThirdPartySignInUpPostOkResult):
            if result.created_new_user:
                user_id = result.user.user_id
                email = result.user.email
                try:
                    res = requests.post(
                        settings.api_data_url + "/auth/postsignup",
                        json={"id": user_id, "email": email},
                    )
                    if res.status_code != 201:  # API error
                        await delete_user(user_id)
                        return None
                except:  # Network error
                    await delete_user(user_id)
                    raise ValueError(
                        "An error occurred while posting the request to api_data_url"
                    )
            else:
                pass  # TODO: some post sign in logic

        return result

    async def emailpassword_sign_in_post(
        form_fields: List[FormField],
        api_options: EmailPasswordAPIOptions,
        user_context: Dict[str, Any],
    ):
        # call the default behaviour as show below
        result = await original_emailpassword_sign_in_post(
            form_fields, api_options, user_context
        )

        if isinstance(result, EmailPasswordSignInPostOkResult):
            pass  # TODO: some post sign in logic

        return result

    async def emailpassword_sign_up_post(
        form_fields: List[FormField],
        api_options: EmailPasswordAPIOptions,
        user_context: Dict[str, Any],
    ):
        # call the default behaviour as show below
        result = await original_emailpassword_sign_up_post(
            form_fields, api_options, user_context
        )

        if isinstance(result, EmailPasswordSignUpPostOkResult):
            user_id = result.user.user_id
            email = result.user.email
            try:
                res = requests.post(
                    settings.api_data_url + "/auth/postsignup",
                    json={"id": user_id, "email": email},
                )
                if res.status_code != 201:  # API error
                    await delete_user(user_id)
                    return None
            except:  # Network error
                await delete_user(user_id)
                raise ValueError(
                    "An error occurred while posting the request to api_data_url"
                )
        return result

    original_implementation.thirdparty_sign_in_up_post = thirdparty_sign_in_up_post
    original_implementation.emailpassword_sign_in_post = emailpassword_sign_in_post
    original_implementation.emailpassword_sign_up_post = emailpassword_sign_up_post
    return original_implementation


if settings.environment == "PROD":
    app = FastAPI(openapi_url=None, redoc_url=None)
    nest_asyncio.apply()  # lambda supertokens_python fix
    mode = "wsgi"
else:
    app = FastAPI()
    mode = "asgi"

init(
    app_info=InputAppInfo(
        app_name="SportsConnect",
        api_domain=settings.api_auth_url,
        website_domain=settings.app_url,
        api_base_path="/auth",
        website_base_path="/auth",
    ),
    supertokens_config=SupertokensConfig(
        # connection_uri="http://localhost:3567", # Self-hosted core.
        connection_uri=settings.connection_uri,
        api_key=settings.api_key,
    ),
    framework="fastapi",
    recipe_list=[
        session.init(
            cookie_secure=settings.cookie_secure,
            cookie_domain=settings.cookie_domain,
            cookie_same_site=settings.cookie_same_site,
        ),
        emailverification.init(mode=settings.email_verification),
        thirdpartyemailpassword.init(
            override=thirdpartyemailpassword.InputOverrideConfig(
                apis=override_thirdpartyemailpassword_apis
            ),
            providers=[
                Google(
                    client_id=settings.google_client_id,
                    client_secret=settings.google_client_secret,
                ),
            ],
        ),
    ],
    mode=mode,
)

app.add_middleware(get_middleware())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.origin_0],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"]
    + get_all_cors_headers(),  # ['fdi-version', 'rid', 'anti-csrf']
)


@app.get("/healthauth")
def check_health():
    return {"health": "healthy (auth)"}


handler = Mangum(app)
