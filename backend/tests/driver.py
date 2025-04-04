import json
import re
import sys
import time
import uuid
from enum import Enum
from typing import assert_never

import requests
import urllib3

from backend.passphrases import Passphrases

LOCAL_SERVER_URL = "http://127.0.0.1:12301"
REMOTE_SERVER_URL = "https://api.ctf.neumaneuma.com"
external_url_pattern = re.compile(
    r"^Challenge failed\. Response body: <!DOCTYPE html>.*"
)


class SQLI:
    class LoginBypass:
        class Vulnerabilities:
            @staticmethod
            def get_login_data(url_prefix: str) -> tuple[str, int]:
                return (f"{url_prefix}/vulnerabilities/sqli1/login/", 200)

        class Patches:
            @staticmethod
            def get_login_data(url_prefix: str) -> tuple[str, int, dict[str, str]]:
                return (
                    f"{url_prefix}/patches/sqli1/login/",
                    403,
                    {"detail": "Login failed"},
                )

    class SecondOrder:
        class Vulnerabilities:
            @staticmethod
            def get_register_data(url_prefix: str) -> tuple[str, int, str]:
                return (
                    f"{url_prefix}/vulnerabilities/sqli2/register/",
                    200,
                    "Successfully registered",
                )

            @staticmethod
            def get_change_password_data(url_prefix: str) -> tuple[str, int]:
                return (f"{url_prefix}/vulnerabilities/sqli2/change_password/", 200)

        class Patches:
            @staticmethod
            def get_register_data(url_prefix: str) -> tuple[str, int, str]:
                return (
                    f"{url_prefix}/patches/sqli2/register/",
                    200,
                    "Successfully registered",
                )

            @staticmethod
            def get_change_password_data(url_prefix: str) -> tuple[str, int, str]:
                return (
                    f"{url_prefix}/patches/sqli2/change_password/",
                    200,
                    "Successfully changed password",
                )


class SSRF:
    class Webhook:
        class Vulnerabilities:
            @staticmethod
            def get_submit_webhook_url(url_prefix: str) -> str:
                return f"{url_prefix}/vulnerabilities/ssrf1/submit_webhook/"

        class Patches:
            @staticmethod
            def get_submit_webhook_url(url_prefix: str) -> str:
                return f"{url_prefix}/patches/ssrf1/submit_webhook/"

    class LocalFileInclusion:
        class Vulnerabilities:
            @staticmethod
            def get_submit_api_url(url_prefix: str) -> str:
                return f"{url_prefix}/vulnerabilities/ssrf2/submit_api_url/"

        class Patches:
            @staticmethod
            def get_submit_api_url(url_prefix: str) -> str:
                return f"{url_prefix}/patches/ssrf2/submit_api_url/"


class State(Enum):
    VULNERABLE = "vulnerable"
    PATCHED = "patched"


def check_response(
    *,
    expected_status_code: int,
    actual_status_code: int,
    expected_response: str | dict[str, bool] | dict[str, str],
    actual_response: str | dict[str, bool] | dict[str, str],
    url: str = "",
    appended_custom_msg: str = "",
) -> bool:
    assert type(expected_response) is type(actual_response), (
        f"Expected and actual response types do not match. Expected: {type(expected_response)}, Actual: {type(actual_response)}.\n\t- Expected response: {expected_response}\n\t- Actual response: {actual_response}"
    )
    success = (
        expected_status_code == actual_status_code
        and expected_response == actual_response
    )
    if success:
        msg = f"\tPASSED {appended_custom_msg}"
    else:
        msg = f"\tFAILED {appended_custom_msg}"
        if expected_status_code != actual_status_code:
            msg += f"\n\t- Expected status code: {expected_status_code}\n\t- Actual_status_code: {actual_status_code}"
        if expected_response != actual_response:
            msg += f"\n\t- Expected response: {expected_response}\n\t- Actual response: {actual_response}"

    if url:
        msg += f"\n\t- URL: {url}"

    print(msg)
    return success


def test_static_routes(url_prefix: str, verify: bool) -> list[bool]:
    base_url = f"{url_prefix}"
    health_url = f"{url_prefix}/health"
    r = requests.get(base_url, verify=verify)
    print("Testing root endpoint...")
    r1 = check_response(
        expected_status_code=200,
        actual_status_code=r.status_code,
        expected_response='"👋 🌎"',
        actual_response=r.text,
    )
    r = requests.get(health_url, verify=verify)
    print("Testing health check...")
    r2 = check_response(
        expected_status_code=200,
        actual_status_code=r.status_code,
        expected_response='"OK"',
        actual_response=r.text,
    )
    return [r1, r2]


def test_submission(
    challenge: Passphrases, secret: str, *, url_prefix: str, verify: bool
) -> bool:
    url = f"{url_prefix}/submission"
    data = {"secret": secret, "challenge": challenge.name}
    r = requests.post(url, json=data, verify=verify)
    print(f"Testing submission for challenge {challenge.name}...")
    return check_response(
        expected_status_code=200,
        actual_status_code=r.status_code,
        expected_response={"result": True},
        actual_response=r.json(),
    )


def sqli_login_bypass(state: State, *, url_prefix: str, verify: bool) -> list[bool]:
    expected_response: str | dict[str, str]
    username = "administrator"
    password = "' OR 'a' = 'a"
    data = {"username": username, "password": password}

    match state:
        case State.VULNERABLE:
            url, status_code = SQLI.LoginBypass.Vulnerabilities.get_login_data(
                url_prefix
            )
        case State.PATCHED:
            url, status_code, patched_expected_response = (
                SQLI.LoginBypass.Patches.get_login_data(url_prefix)
            )
        case _:
            assert_never(state)

    r = requests.post(url, json=data, verify=verify)
    actual_response = r.json()

    # Since the passphrases are generated dynamically, we can't know a priori what
    # the passphrases are. So we check that the submission api returns true for the
    # vulnerable endpoint (since that will confirm that the challenge is working
    # correctly)
    expected_response = (
        patched_expected_response if state == State.PATCHED else actual_response
    )

    response = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=actual_response,
    )

    responses = [response]

    if state == State.VULNERABLE:
        submission_response = test_submission(
            Passphrases.sqli1, actual_response, url_prefix=url_prefix, verify=verify
        )
        responses.append(submission_response)

    return responses


def sqli_second_order(state: State, *, url_prefix: str, verify: bool) -> list[bool]:
    password = str(uuid.uuid4())

    match state:
        case State.VULNERABLE:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Vulnerabilities.get_register_data(url_prefix)
            )
        case State.PATCHED:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Patches.get_register_data(url_prefix)
            )
        case _:
            assert_never(state)

    username = "batman';-- "
    data = {"username": username, "password": password}
    r = requests.post(url, json=data, verify=verify)
    first_check = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=r.json(),
        appended_custom_msg="(1/2)",
    )

    match state:
        case State.VULNERABLE:
            url, status_code = (
                SQLI.SecondOrder.Vulnerabilities.get_change_password_data(url_prefix)
            )
        case State.PATCHED:
            url, status_code, patched_expected_response = (
                SQLI.SecondOrder.Patches.get_change_password_data(url_prefix)
            )
        case _:
            assert_never(state)

    data = {"old": password, "new": password, "new_verify": password}
    r = requests.post(url, json=data, cookies=r.cookies, verify=verify)
    actual_response = r.json()

    # Since the passphrases are generated dynamically, we can't know a priori what
    # the passphrases are. So we check that the submission api returns true for the
    # vulnerable endpoint (since that will confirm that the challenge is working
    # correctly)
    expected_response = (
        patched_expected_response if state == State.PATCHED else actual_response
    )

    second_check = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=actual_response,
        appended_custom_msg="(2/2)",
    )

    responses = [first_check, second_check]

    if state == State.VULNERABLE:
        submission_response = test_submission(
            Passphrases.sqli2, actual_response, url_prefix=url_prefix, verify=verify
        )
        responses.append(submission_response)

    return responses


def ssrf_webhook(state: State, *, url_prefix: str, verify: bool) -> list[bool]:
    submission_secret: str
    match state:
        case State.VULNERABLE:
            url = SSRF.Webhook.Vulnerabilities.get_submit_webhook_url(url_prefix)
            file_name = "backend/tests/ssrf_webhook_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.Webhook.Patches.get_submit_webhook_url(url_prefix)
            file_name = "backend/tests/ssrf_webhook_test_urls_patched.json"
        case _:
            assert_never(state)

    with open(file_name) as test_urls:
        expected_responses: list[dict[str, str] | dict[str, dict[str, str]]] = (
            json.load(test_urls)
        )

    all_response_checks = []
    for i, er in enumerate(expected_responses):
        payload_url = er["url"]
        assert isinstance(payload_url, str), "URL is not an string"
        raw_status_code = er["status_code"]
        assert isinstance(raw_status_code, str), "Status code is not an string"
        status_code = int(raw_status_code)
        expected_response = er["response"]

        data = {"url": payload_url}
        r = requests.post(url, json=data, verify=verify)
        actual_response = r.json()

        # Hacky way of dealing with not being able to access python from the json file
        if (
            isinstance(expected_response, str)
            and expected_response == "Passphrases.ssrf1.value"
        ):
            expected_response = actual_response
            submission_secret = actual_response
        elif (
            isinstance(actual_response, dict)
            and "detail" in actual_response
            and external_url_pattern.match(actual_response["detail"])
        ):
            actual_response["detail"] = (
                "Challenge failed. Response body: <!DOCTYPE html>"
            )

        is_correct_response = check_response(
            expected_status_code=status_code,
            actual_status_code=r.status_code,
            expected_response=expected_response,
            actual_response=actual_response,
            url=payload_url,
            appended_custom_msg=f"({i + 1}/{len(expected_responses)})",
        )
        all_response_checks.append(is_correct_response)
        if not is_correct_response:
            break

    # Since the passphrases are generated dynamically, we can't know a priori what
    # the passphrases are. So we check that the submission api returns true for the
    # vulnerable endpoint (since that will confirm that the challenge is working
    # correctly)
    if state == State.VULNERABLE:
        submission_response = test_submission(
            Passphrases.ssrf1, submission_secret, url_prefix=url_prefix, verify=verify
        )
        all_response_checks.append(submission_response)

    return all_response_checks


def ssrf_local_file_inclusion(
    state: State, *, url_prefix: str, verify: bool
) -> list[bool]:
    submission_secret: str
    cat_coin_price_pattern = re.compile(
        r"\"Price at \d{2}:\d{2}:\d{2}\.\d{6} - \$\d+\.\d+\""
    )

    match state:
        case State.VULNERABLE:
            url = SSRF.LocalFileInclusion.Vulnerabilities.get_submit_api_url(url_prefix)
            file_name = "backend/tests/ssrf_lfi_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.LocalFileInclusion.Patches.get_submit_api_url(url_prefix)
            file_name = "backend/tests/ssrf_lfi_test_urls_patched.json"
        case _:
            assert_never(state)

    with open(file_name) as test_urls:
        expected_responses: list[dict[str, str] | dict[str, dict[str, str]]] = (
            json.load(test_urls)
        )

    all_response_checks = []
    for i, er in enumerate(expected_responses):
        payload_url = er["url"]
        assert isinstance(payload_url, str), "URL is not an string"
        raw_status_code = er["status_code"]
        assert isinstance(raw_status_code, str), "Status code is not an string"
        status_code = int(raw_status_code)
        expected_response = er["response"]

        data = {"url": payload_url}
        r = requests.post(url, json=data, verify=verify)

        actual_response = r.json()

        # Hacky way of dealing with not being able to access python from the json file
        if (
            isinstance(expected_response, str)
            and expected_response == "Passphrases.ssrf2.value"
        ):
            expected_response = actual_response
            submission_secret = actual_response
        elif isinstance(actual_response, str) and cat_coin_price_pattern.match(
            actual_response
        ):
            actual_response = "Cat coin price"
        elif (
            isinstance(actual_response, dict)
            and "detail" in actual_response
            and external_url_pattern.match(actual_response["detail"])
        ):
            actual_response["detail"] = (
                "Challenge failed. Response body: <!DOCTYPE html>"
            )

        is_correct_response = check_response(
            expected_status_code=status_code,
            actual_status_code=r.status_code,
            expected_response=expected_response,
            actual_response=actual_response,
            url=payload_url,
            appended_custom_msg=f"({i + 1}/{len(expected_responses)})",
        )
        all_response_checks.append(is_correct_response)
        if not is_correct_response:
            break

    if state == State.VULNERABLE:
        submission_response = test_submission(
            Passphrases.ssrf2, submission_secret, url_prefix=url_prefix, verify=verify
        )
        all_response_checks.append(submission_response)

    return all_response_checks


def get_cli_arguments() -> tuple[str, bool]:
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    assert len(opts) == 1, "Only one flag can be provided"
    message = "Overriding default: "

    if "-v" in opts:
        verify = True
        print(f"{message} using verified requests")
    else:
        verify = False
        print(f"{message} using unverified requests")

    if "-r" in opts:
        url_prefix = REMOTE_SERVER_URL
        print(f"{message} using remote server")
    elif "-l" in opts:
        url_prefix = LOCAL_SERVER_URL
        print(f"{message} using local server")
    elif "-c" in opts:
        args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        if not args:
            raise ValueError("Custom URL must be provided with -c flag")
        custom_url = args[0]
        url_prefix = (
            custom_url if custom_url.startswith("http") else f"https://{custom_url}"
        )
        print(f"{message} using custom server {url_prefix}")
    else:
        raise ValueError("Invalid flag provided")

    return url_prefix, verify


if __name__ == "__main__":
    url_prefix, verify = get_cli_arguments()
    start_time = round(time.time() * 1000)
    print("Starting functional test...\n\n")
    results = []

    if not verify:
        # Disable loud warnings if not verifying TLS certificate
        urllib3.disable_warnings()

    print("Testing static routes...")
    results.extend(test_static_routes(url_prefix=url_prefix, verify=verify))

    for state in State:
        print(f"Testing {state.name} state for SQLi login bypass...")
        results.extend(sqli_login_bypass(state, url_prefix=url_prefix, verify=verify))

        print(f"Testing {state.name} state for SQLi second order...")
        results.extend(sqli_second_order(state, url_prefix=url_prefix, verify=verify))
        print(f"Testing {state.name} state for SSRF webhook...")
        results.extend(ssrf_webhook(state, url_prefix=url_prefix, verify=verify))

        print(f"Testing {state.name} state for SSRF local file inclusion...")
        results.extend(
            ssrf_local_file_inclusion(state, url_prefix=url_prefix, verify=verify)
        )

    stop_time = round(time.time() * 1000)
    run_time = (stop_time - start_time) / 1000
    print(
        f"\n\nFinished running {len(results)} functional tests. Run time: {run_time} seconds"
    )

    assert all(results), (
        f"There were {len([r for r in results if not r])} failed tests 😭"
    )
