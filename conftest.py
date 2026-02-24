import pytest
import os
from playwright.sync_api import sync_playwright, APIRequestContext

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


