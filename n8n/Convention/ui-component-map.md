# YOUngChat QA — UI 컴포넌트 맵

블랙박스 TC 작성 시 본 문서를 기준으로 UI 구성 요소를 참조한다.
코드에서 확정되지 않는 UI는 사용자에게 캡처를 요청한다.

---

## 화면 전환 구조

```
/login
/signup
/ (Main)
  ├── Header
  ├── Sidebar (열림/닫힘 토글)
  │   ├── [Friend] 탭
  │   ├── [Chat] 탭
  │   ├── [MyPage] 탭
  │   └── [Logout] 버튼
  ├── SecondColumn (카테고리별 목록 영역)
  │   ├── 상단 고정: 로그인 유저 프로필 이미지 + "반갑습니다 {username} 님"
  │   ├── category = friend → Friend 컴포넌트
  │   ├── category = chat → Chat 컴포넌트
  │   └── category = myPage → MyPage 컴포넌트
  ├── MainBody (메인 콘텐츠 영역)
  │   ├── mainBody = chatRoom → Chatroom
  │   ├── mainBody = profile → Profile
  │   ├── mainBody = editProfile → EditProfile
  │   ├── mainBody = editPassword → EditPassword
  │   ├── mainBody = friendAdd → FriendAdd
  │   ├── mainBody = friendSearch → FriendSearch
  │   └── mainBody = null/default → 빈 화면
  ├── Snackbar (타 채팅방 메시지 수신 시 상단 중앙 노출)
  └── Footer
```

**초기 진입 시 기본 카테고리:** `friend` (Sidebar 진입 시 setCategory("friend") 강제 설정)

---

## 1. 로그인 화면 `/login`

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [Email Address] | TextField (required) | 항상 활성 | |
| [Password] | TextField (required, type=password) | 항상 활성 | |
| [Login] | Button | 항상 활성 | 클릭 시 login API 호출 |
| 회원가입 링크 | Link | 항상 활성 | `/signup`으로 이동 |

**동작 분기:**
- 로그인 성공: "로그인에 성공하였습니다!" alert → `/` 이동, AccessToken/RefreshToken 쿠키 저장
- 로그인 실패: "이메일 혹은 비밀번호를 확인해주세요" alert
- 로그인 화면 진입 시: 기존 토큰 자동 삭제, localStorage 초기화

---

## 2. 회원가입 화면 `/signup`

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [Username] | TextField (required) | 항상 활성 | 영소문자/한글/숫자 2~10자 (helperText 표시) |
| [Email Address] | TextField (required) | 이메일 인증 완료 전 활성, 완료 후 disabled | |
| [인증] | Button | 항상 활성 | 클릭 시 이메일 중복 확인 → 인증 다이얼로그 오픈 |
| 이메일 인증 다이얼로그 | Dialog | [인증] 클릭 시 오픈 | |
| └ [Code] | TextField (required) | 다이얼로그 내 | 인증 코드 입력 |
| └ [확인] | Button | 다이얼로그 내 | 코드 검증 API 호출 |
| [Password] | TextField (required, type=password) | 항상 활성 | 영소문자/숫자/특수문자 8~15자 (helperText 표시) |
| [Sign Up] | Button | 항상 활성 (disabled 조건 없음) | signupLoading 상태일 때 disabled |
| 로그인 링크 | Link | 항상 활성 | `/login`으로 이동 |

**동작 분기:**
- [인증] 클릭 시:
  - 이메일 형식 불일치: "이메일 형식이 올바르지 않습니다." alert (프론트 정규식 검증)
  - 이미 가입된 이메일: "이미 존재하는 이메일 입니다." alert
  - 정상 이메일: 다이얼로그 오픈 + "이메일에 코드가 전송되었습니다." alert + 인증 메일 발송
- 인증 코드 [확인] 클릭 시:
  - 코드 일치: 다이얼로그 닫힘, 이메일 필드 disabled 전환
  - 코드 불일치: 예외 처리 (서버 응답)
- [Sign Up] 클릭 시:
  - 성공: "회원가입을 축하드립니다!" alert → `/login` 이동
  - 실패: 유효성 검사 실패 메시지 alert 다중 출력 (response[i].message 순회)

---

## 3. 메인 화면 `/` — Header

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [햄버거 메뉴] 아이콘 | IconButton | Sidebar 닫힘 상태일 때만 노출 | 클릭 시 Sidebar 열림 |
| [YOUngChat] 타이틀 | Link | 항상 활성 | `/`로 이동 |

---

## 4. 메인 화면 `/` — Sidebar

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [ChevronLeft/Right] 아이콘 | IconButton | 항상 활성 | 열림: ChevronLeft, 닫힘: ChevronRight |
| [Friend] 탭 | ListItemButton | 항상 활성 | category = friend, mainBody = null |
| [Chat] 탭 | ListItemButton | 항상 활성 | category = chat, mainBody = null |
| [MyPage] 탭 | ListItemButton | 항상 활성 | category = myPage, mainBody = null |
| [Logout] 버튼 | ListItemButton | 항상 활성 | logout API → localStorage 초기화 → `/login` 이동 → "로그아웃을 성공하였습니다." alert → 토큰 삭제 |

**Sidebar 열림/닫힘:**
- 열림 상태: 아이콘 + 텍스트 표시 (width: 240px)
- 닫힘 상태: 아이콘만 표시 (width: calc(theme.spacing(8) + 1px))

---

## 5. 메인 화면 `/` — SecondColumn (상단 고정 영역)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| 프로필 Avatar | Avatar | 항상 노출 | 로그인 유저 프로필 이미지 |
| "반갑습니다" / "{username} 님" | Typography | 항상 노출 | getProfile API로 username 조회 |

---

## 6. SecondColumn — Friend 탭

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| "Friend" 타이틀 | Typography | 항상 노출 | |
| [친구 추가] | ListItemButton | 항상 활성 | mainBody = friendAdd |
| [친구 검색] | ListItemButton | 항상 활성 | mainBody = friendSearch |
| "친구 목록" 타이틀 | Typography | 항상 노출 | |
| 친구 목록 아이템 | ListItemButton | 친구 존재 시 노출 | 클릭 시 친구 상세 다이얼로그 오픈 |
| 친구 상세 다이얼로그 | Dialog | 친구 아이템 클릭 시 오픈 | |
| └ 프로필 Avatar (300x300) | Avatar | 다이얼로그 내 | |
| └ {username} | Typography | 다이얼로그 내 | |
| └ [대화하기] | Button | 다이얼로그 내 | 1:1 채팅방 생성/재사용 → chatRoom으로 이동 |
| └ [친구삭제] | Button (error) | 다이얼로그 내 | deleteFriend API → alert → 페이지 리로드 |

---

## 7. SecondColumn — Chat 탭

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| "Chat" 타이틀 | Typography | 항상 노출 | |
| [+] 아이콘 버튼 | IconButton | 항상 활성 | 친구 목록 조회 → 채팅방 생성 다이얼로그 오픈 |
| 채팅방 생성 다이얼로그 | Dialog | [+] 클릭 시 오픈 | |
| └ 친구 목록 (Checkbox) | ListItemButton | 다이얼로그 내 | 다중 선택 가능 |
| └ [생성하기] | Button | 다이얼로그 내 | 선택 0명: 다이얼로그 닫힘 / 1명: 1:1 / 2명 이상: 그룹 |
| 채팅방 목록 | InfiniteScroll | 채팅방 존재 시 | 무한 스크롤, 높이 65vh |
| └ 채팅방 타이틀 | Typography | 각 아이템 | 말줄임 처리 (overflow: ellipsis) |
| └ 마지막 메시지 | Typography (gray) | 각 아이템 | 삭제된 메시지: "삭제된 메세지입니다" |

**채팅방 생성 분기:**
- 친구 1명 선택: `POST /api/v1/chat-rooms/personal` → 기존 방 재사용 또는 신규 생성
- 친구 2명 이상 선택: `POST /api/v1/chat-rooms/group` → 그룹 채팅방 신규 생성
- 0명 선택 후 [생성하기]: 다이얼로그 닫힘, 채팅방 생성 없음

---

## 8. SecondColumn — MyPage 탭

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| "My Page" 타이틀 | Typography | 항상 노출 | |
| [사용자 정보 변경] | ListItemButton | 항상 활성 | mainBody = profile |
| [비밀번호 변경] | ListItemButton | 항상 활성 | mainBody = editPassword |

---

## 9. MainBody — 채팅방 (Chatroom)

### ChatHeader

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [EditNote] 아이콘 버튼 | IconButton | 항상 활성 | 채팅방 제목 수정 다이얼로그 오픈 |
| 채팅방 제목 | Typography | 항상 노출 | selectedChatRoomTitle |
| [채팅방 나가기] | Button | 항상 활성 | 나가기 확인 다이얼로그 오픈 |
| 제목 수정 다이얼로그 | Dialog | EditNote 클릭 시 오픈 | |
| └ 제목 입력 TextField | TextField | 다이얼로그 내 | 현재 제목 기본값 |
| └ [수정] | Button | 다이얼로그 내 | editChatRoom API → "변경이 완료되었습니다." alert |
| 나가기 확인 다이얼로그 | Dialog | [채팅방 나가기] 클릭 시 오픈 | |
| └ [취소하기] | Button | 다이얼로그 내 | 다이얼로그 닫힘 |
| └ [나가기] | Button (error) | 다이얼로그 내 | leaveChatRoom API → "채팅방을 나갔습니다." alert → 목록 갱신 → mainBody 초기화 |

### MessageList

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| 메시지 목록 | InfiniteScroll (역방향) | 항상 노출 | 높이 60vh, 역방향 무한 스크롤 |
| 타인 메시지 (좌측) | Paper (blue, #b3e5fc) | userId ≠ 나 | |
| └ Avatar (30x30) | Avatar | showAvatarAndName = true일 때만 노출 | 연속 메시지 시 미노출 |
| └ username | Typography (caption) | showAvatarAndName = true일 때만 노출 | |
| └ 메시지 시간 | Typography (caption) | 항상 노출 | HH:MM:SS 포맷 |
| └ 삭제된 메시지 | Typography | isDeleted = true | "삭제된 메세지입니다." 표시 |
| 내 메시지 (우측) | Paper (yellow, #f0f4c3) | userId = 나 | 클릭 시 삭제 다이얼로그 오픈 |
| └ 메시지 시간 | Typography (caption) | 항상 노출 | |
| 타인 아바타 클릭 | Dialog | Avatar 클릭 시 오픈 | |
| └ 프로필 Avatar (300x300) | Avatar | 다이얼로그 내 | |
| └ username | Typography | 다이얼로그 내 | |
| └ [친구 추가] | Button | 다이얼로그 내 | addFriend API → "친구 추가 되었습니다." alert → 페이지 리로드 |
| 메시지 삭제 다이얼로그 | Dialog | 내 메시지 클릭 시 오픈 | |
| └ "메시지를 삭제하시겠습니까?" | DialogTitle | 다이얼로그 내 | |
| └ [확인] | Button (error) | 다이얼로그 내 | STOMP publish → 삭제 처리 |
| └ [취소] | Button | 다이얼로그 내 | 다이얼로그 닫힘 |

### TextareaChat

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [보낼 메세지를 입력해주세요] | InputBase | 항상 활성 | |
| [Send] 아이콘 버튼 | IconButton | 항상 활성 | 공백 메시지: 전송 차단 (trim() === '') |

**메시지 전송 동작:**
- 정상 전송: STOMP publish → 입력창 초기화 → chatStatus 토글 (메시지 목록 갱신)
- 공백 메시지: return으로 차단, 전송 없음
- WebSocket 미연결 상태: stompClient 없으면 전송 불가

---

## 10. MainBody — 프로필 조회 (Profile)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| 프로필 Avatar (200x200) | Avatar | 항상 노출 | getProfile API로 이미지 조회 |
| {username} | Typography (h4, bold) | 항상 노출 | |
| {email} | Typography | 항상 노출 | |
| [프로필 변경] | Button | 항상 활성 | mainBody = editProfile |

---

## 11. MainBody — 프로필 수정 (EditProfile)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| 프로필 Avatar (200x200) | Avatar + Badge | 항상 노출 | 이미지 선택 전: 기존 이미지, 선택 후: 미리보기 |
| [Edit] 아이콘 Badge | IconButton | 항상 활성 | 클릭 시 파일 선택창 오픈 (png, jpeg만 허용) |
| [Username] | TextField (required) | 항상 활성 | 현재 username 기본값 |
| [확인] | Button | 항상 활성 | editProfile API → "프로필 수정이 완료되었습니다." alert → mainBody = profile |

**이미지 업로드 조건:**
- 허용 형식: image/png, image/jpeg
- 파일 미선택 시 기존 이미지 유지 (multipartFile null 처리)

---

## 12. MainBody — 비밀번호 변경 (EditPassword)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [이전 비밀번호] | TextField (required, type=password) | 항상 활성 | |
| [새로운 비밀번호] | TextField (required, type=password) | 항상 활성 | |
| [새로운 비밀번호 확인] | TextField (required, type=password) | 항상 활성 | |
| [확인] | Button | 항상 활성 | editPassword API |

**동작 분기:**
- 성공: "비밀번호 수정이 완료되었습니다." alert → mainBody = profile
- 실패: 유효성 검사 실패 메시지 alert 다중 출력 (error.response.data.data[i].message 순회)

---

## 13. MainBody — 친구 추가 (FriendAdd)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [Email] | TextField | 항상 활성 | 이메일 입력 |
| [이메일 검색] | Button | 항상 활성 | userSearch API 호출 |
| 검색 결과 영역 | 조건부 렌더링 | open = true일 때만 노출 | Avatar (300x300) + username + email |
| 검색 결과 Avatar | Avatar (300x300) | 검색 성공 시 | 클릭 시 프로필 다이얼로그 오픈 |
| 프로필 다이얼로그 | Dialog | Avatar 클릭 시 오픈 | |
| └ Avatar (300x300) | Avatar | 다이얼로그 내 | |
| └ {username} | Typography | 다이얼로그 내 | |
| └ [친구 추가] | Button | 다이얼로그 내 | addFriend API → "친구 추가 되었습니다." alert → 페이지 리로드 |

---

## 14. MainBody — 친구 검색 (FriendSearch)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| [name] | TextField | 항상 활성 | keyword 입력 시 즉시 getFriendSearch API 호출 (useEffect) |
| 검색 결과 목록 | ListItem | keyword 비어있지 않을 때 | |
| 친구 상세 다이얼로그 | Dialog | 검색 결과 아이템 클릭 시 오픈 | |
| └ 프로필 Avatar (300x300) | Avatar | 다이얼로그 내 | |
| └ {username} | Typography | 다이얼로그 내 | |
| └ [대화하기] | Button | 다이얼로그 내 | 1:1 채팅방 생성/재사용 → chatRoom 이동 |
| └ [친구삭제] | Button (error) | 다이얼로그 내 | deleteFriend API → alert → 페이지 리로드 |

**실시간 검색 동작:**
- keyword 변경 시마다 useEffect 트리거 → getFriendSearch API 즉시 호출
- keyword 공백 시 결과 목록 초기화

---

## 15. 메인 화면 `/` — Snackbar (알림)

| 컴포넌트 | 타입 | 동작 조건 | 비고 |
|---|---|---|---|
| Snackbar | 상단 중앙 | 타 채팅방 메시지 수신 시 노출 | 3초 자동 닫힘 (autoHideDuration: 3000) |
| └ 채팅방 이름 | Typography (bold) | Snackbar 내 | |
| └ 발신자 Avatar | Avatar | Snackbar 내 | |
| └ 발신자 username | Typography | Snackbar 내 | |
| └ 메시지 내용 | Typography | Snackbar 내 | |
| └ [Close] 아이콘 | IconButton | Snackbar 내 | 수동 닫기 |

**노출 조건:**
- 수신한 메시지의 chatRoomId ≠ 현재 열람 중인 채팅방 ID → Snackbar 노출
- 수신한 메시지의 chatRoomId = 현재 열람 중인 채팅방 ID → Snackbar 미노출