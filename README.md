# AI_Lab

여러 AI 에이전트(Claude Code, Codex, Antigravity, Hermes Agent, Paseo)와 AI 관련 오픈소스를 실험·운영하는 개인 Lab의 **정리 문서 저장소**입니다.
실제 작업물은 로컬(`D:\VSCode_Workspace\02.AI_laboratory`, `D:\MYDrive\19_AI_LAB` 등)에 있고, 이 저장소에는 구성 방법과 활용법을 정리합니다.

## 문서

| 문서 | 내용 |
|---|---|
| [docs/ai-opensource-inventory.md](docs/ai-opensource-inventory.md) | AI 오픈소스·도구 인벤토리(Hermes, Paseo, Ollama, MCP, Codex 등), 구성값, 멀티 에이전트 역할 분담, 활용 시나리오 |
| [docs/rea-reverse-engineering-analysis.md](docs/rea-reverse-engineering-analysis.md) | REA(Reverse Engineering Analysis) — 의심 파일 정적 리버싱 환경 구성, 단계별 절차, 사례 연구, 재사용 플레이북 |
| [docs/hot-opensource-2026-11.md](docs/hot-opensource-2026-11.md) | 2026년 11월 핫 오픈소스(AI 중심) — 트렌드 7개, YouTube·커뮤니티 반응, REA(Reverse Engineer Anything) 집중 분석, 위험 신호, Lab 맞춤 추천, GitHub 실측 데이터 |
| [rea/](rea/) | REA 실행 도구 — `requirements-rea.txt`(툴체인 버전 고정), `new_case.py`(케이스 폴더 생성), `hash_manifest.py`(SHA-256 전후 검증) |

## Lab 공통 원칙

1. 읽기 전용 우선. 설치·적용·삭제는 사람의 승인 후에만 합니다(HITL).
2. 모든 변경은 SHA-256과 실측 용량으로 검증하고, 실행하지 않은 것은 실행했다고 쓰지 않습니다.
3. 에이전트마다 Lab 폴더를 따로 두고, 작업 폴더 이름은 `YYYY-MM-DD_주제_에이전트`로 합니다.
4. 공개 저장소이므로 토큰·계정·개인 경로·원본 악성 샘플은 올리지 않습니다.
