import pytest
import os
from playwright.sync_api import APIRequestContext
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FRONT_URL = os.getenv("FRONT_URL")

TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
TEST_USER2_EMAIL = os.getenv("TEST_USER2_EMAIL")
TEST_USER2_PASSWORD = os.getenv("TEST_USER2_PASSWORD")

# 인증 없이 사용할 수 있는 API context (로그인, 회원가입용)
# playwright fixture를 인자로 받아서 사용 (sync_playwright 직접 호출 시 asyncio 충돌 발생)
@pytest.fixture(scope="session")
def api_request_context(playwright):
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()

# USER1 JWT 토큰 발급
@pytest.fixture(scope="session")
def auth_tokens_user1(api_request_context):
    response = api_request_context.post(
        "users/login",
        data={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    )
    assert response.status == 200, "USER1 로그인 실패 - .env 파일에서 계정 정보 확인"
    access_token = response.headers.get("Accesstoken")
    refresh_token = response.headers.get("Refreshtoken")
    return {"access_token":access_token, "refresh_token":refresh_token}

# USER2 JWT 토큰 발급
@pytest.fixture(scope="session")
def auth_tokens_user2(api_request_context):
    response = api_request_context.post(
        "users/login",
        data={"email":TEST_USER2_EMAIL, "password":TEST_USER2_PASSWORD}
    )
    assert response.status == 200, "USER2 로그인 실패 - .env 파일에서 계정 정보 확인"
    access_token = response.headers.get("accesstoken")
    refresh_token = response.headers.get("refreshtoken")
    return {"access_token":access_token, "refresh_token": refresh_token}


# USER1 인증된 API context
@pytest.fixture(scope="session")
def user1_api(playwright, auth_tokens_user1):
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"AccessToken": auth_tokens_user1["access_token"]}
    )
    yield context
    context.dispose() # Java @AfterAll과 동일


# USER2 인증된 API context
@pytest.fixture(scope="session")
def user2_api(playwright, auth_tokens_user2):
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"AccessToken": auth_tokens_user2["access_token"]}
    )
    yield context
    context.dispose()


# 테스트 시작 전 user1 -> user2 친구 추가 + 채팅방 생성
@pytest.fixture(scope="session")
def setup_chat(user1_api, user2_api):
    # user2의 userId 조회
    res = user2_api.get("users/profile")
    assert res.status == 200, "user2 프로필 조회 실패"
    user2_id = res.json()["data"]["userId"]

    # user1 -> user2 친구 추가 (이미 친구면 409 무시)
    friend_res = user1_api.post(f"friends/{user2_id}")
    assert friend_res.status in [200, 409], "친구 추가 실패"

    # user1 기준으로 user2와 개인 채팅방 생성 (이미 있으면 기존 채팅방 반환)
    chat_res = user1_api.post(
        "/chat-rooms/personal",
        json={"friendId": user2_id}
    )
    assert chat_res.status == 200, "채팅방 생성 실패"

    return {
        "user2_id": user2_id,
        "chat_room_id": chat_res.json()["data"]["chatRoomId"],
        "chat_room_title": chat_res.json()["data"]["title"]
    }