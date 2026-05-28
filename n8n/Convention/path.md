# YOUngChat QA — 기능별 코드 파일 경로 매핑

TC 작성 시 코드 분석이 필요한 경우 본 문서를 기준으로 파일 경로를 참조한다.
경로가 명시되지 않은 기능이거나 매핑이 불명확한 경우, 추론하지 않고 사용자에게 파일 경로를 요청한다.

---

## Repository 정보

- **Backend:** `https://github.com/Just-Clover/YOUng-chat-backend`
- **Frontend:** `https://github.com/Just-Clover/YOUng-chat-frontend`
- **Backend Base Path:** `src/main/java/com/clover/youngchat/domain/`
- **Frontend Base Path:** `src/`

---

## 1. 회원 (User)

| 기능 | Backend | Frontend |
|---|---|---|
| 이메일 중복 확인 | `domain/user/controller/UserController.java` `domain/user/service/query/UserQueryService.java` | `page/Signup.jsx` |
| 이메일 인증 코드 발송 | `domain/user/controller/UserController.java` `domain/user/service/command/UserCommandService.java` `domain/auth/service/EmailAuthService.java` | `page/Signup.jsx` |
| 이메일 인증 코드 확인 | `domain/user/controller/UserController.java` `domain/user/service/command/UserCommandService.java` `domain/auth/service/EmailAuthService.java` | `page/Signup.jsx` |
| 회원가입 | `domain/user/controller/UserController.java` `domain/user/service/command/UserCommandService.java` | `page/Signup.jsx` |
| 프로필 조회 | `domain/user/controller/UserController.java` `domain/user/service/query/UserQueryService.java` | `component/mainbody/Profile.jsx` `component/category/MyPage.jsx` |
| 프로필 검색 (이메일) | `domain/user/controller/UserController.java` `domain/user/service/query/UserQueryService.java` | `component/mainbody/FriendAdd.jsx` |
| 프로필 수정 | `domain/user/controller/UserController.java` `domain/user/service/command/UserCommandService.java` | `component/mainbody/EditProfile.jsx` |
| 비밀번호 변경 | `domain/user/controller/UserController.java` `domain/user/service/command/UserCommandService.java` | `component/mainbody/EditPassword.jsx` |

---

## 2. 인증 (Auth)

| 기능 | Backend | Frontend |
|---|---|---|
| 로그인 | `global/security/` (JWT 필터 처리) | `page/Login.jsx` |
| 로그아웃 | `domain/auth/service/BlacklistService.java` | `component/Sidebar.jsx` |
| 토큰 블랙리스트 검증 | `domain/auth/service/BlacklistService.java` | - |
| 이메일 인증 상태 관리 | `domain/auth/service/EmailAuthService.java` | `page/Signup.jsx` |

---

## 3. 채팅 (Chat)

| 기능 | Backend | Frontend |
|---|---|---|
| 메시지 전송 | `domain/chat/controller/ChatController.java` `domain/chat/service/command/ChatCommandService.java` | `component/mainbody/chatroom/TextareaChat.jsx` |
| 메시지 삭제 | `domain/chat/controller/ChatController.java` `domain/chat/service/command/ChatCommandService.java` | `component/mainbody/chatroom/MessageList.jsx` |
| 메시지 목록 렌더링 | - | `component/mainbody/chatroom/MessageList.jsx` |
| 실시간 수신 / Snackbar 알림 | `domain/chat/service/command/ChatCommandService.java` | `component/MainBody.jsx` `component/SecondColumn.jsx` |

---

## 4. 채팅방 (ChatRoom)

| 기능 | Backend | Frontend |
|---|---|---|
| 1:1 채팅방 생성 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/command/ChatRoomCommandService.java` | `component/category/Chat.jsx` `component/mainbody/friend/FriendSearch.jsx` |
| 그룹 채팅방 생성 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/command/ChatRoomCommandService.java` | `component/category/Chat.jsx` |
| 채팅방 목록 조회 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/query/ChatRoomQueryService.java` | `component/category/Chat.jsx` |
| 채팅방 상세 조회 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/query/ChatRoomQueryService.java` | `component/mainbody/Chatroom.jsx` `component/mainbody/chatroom/ChatHeader.jsx` |
| 채팅방 페이지네이션 조회 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/query/ChatRoomQueryService.java` | `component/mainbody/Chatroom.jsx` |
| 채팅방 수정 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/command/ChatRoomCommandService.java` | `component/mainbody/chatroom/ChatHeader.jsx` |
| 채팅방 나가기 | `domain/chatroom/controller/ChatRoomController.java` `domain/chatroom/service/command/ChatRoomCommandService.java` | `component/mainbody/chatroom/ChatHeader.jsx` |

---

## 5. 친구 (Friend)

| 기능 | Backend | Frontend |
|---|---|---|
| 친구 목록 조회 | `domain/friend/controller/FriendController.java` `domain/friend/service/query/FriendQueryService.java` | `component/category/Friend.jsx` |
| 친구 검색 | `domain/friend/controller/FriendController.java` `domain/friend/service/query/FriendQueryService.java` | `component/mainbody/friend/FriendSearch.jsx` |
| 친구 추가 (이메일 검색) | `domain/friend/controller/FriendController.java` `domain/friend/service/command/FriendCommandService.java` | `component/mainbody/friend/FriendAdd.jsx` |
| 친구 추가 (채팅방 내) | `domain/friend/controller/FriendController.java` `domain/friend/service/command/FriendCommandService.java` | `component/mainbody/chatroom/MessageList.jsx` |
| 친구 삭제 | `domain/friend/controller/FriendController.java` `domain/friend/service/command/FriendCommandService.java` | `component/category/Friend.jsx` `component/mainbody/friend/FriendSearch.jsx` |