import pytest
import os
from playwright.sync_api import sync_playwright, APIRequestContext
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FRONT_URL = os.getenv("FRONT_URL")

TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
TEST_USER2_EMAIL = os.getenv("TEST_USER2_EMAIL")
TEST_USER2_PASSWORD = os.getenv("TEST_USER2_PASSWORD")

# 인증 없이 사용할 수 있는 API context (로그인, 회원가입용)
@pytest.fixture(scope="session")
def api_request_context():
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=BASE_URL)
        yield request_context
        request_context.dispose()

# USER1 JWT 토큰 발급
@pytest.fixture(scope="session")
def auth_tokens_user1(api_request_context):
    response = api_request_context.post(
        "/users/login",
        data={"email": TEST_USER_EMAIL, "password": TEST_USER2_PASSWORD}
    )
    assert response.status == 200, "USER1 로그인 실패 - .env 파일에서 계정 정보 확인"
    access_token = response.headers.get("accesstoken")
    refresh_token = response.headers.get("refreshtoken")
    return {"access_token:":access_token, "refresh_token":refresh_token}

# USER2 JWT 토큰 발급
@pytest.fixture(scope="session")
def auth_tokens_user2(api_request_context):
    response = api_request_context.post(
        "/users/login",
        data={"email":TEST_USER2_EMAIL, "password":TEST_USER2_PASSWORD}
    )
    assert response.status == 200, "USER2 로그인 실패 - .env 파일에서 계정 정보 확인"
    access_token = response.headers.get("accesstoken")
    refresh_token = response.headers.get("refreshtoken")
    return {"access_token":access_token, "refresh_token": refresh_token}

#

