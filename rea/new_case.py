#!/usr/bin/env python3
"""Create an REA case folder skeleton (no analysis is run).

  python new_case.py <diagnostics_root> <slug> [--date YYYY-MM-DD] [--agent Codex]

Example:
  python new_case.py D:\\VSCode_Workspace\\90.diagnostics account_compromise
  -> D:\\VSCode_Workspace\\90.diagnostics\\2026-10-22_account_compromise\\

Existing files are never overwritten.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

STAGES = {
    "collect": "1단계 읽기 전용 수집 결과(*.json). 설정 변경 없음.",
    "quarantine": "격리본 NN_<원래이름>.quarantined. 실행·복원·백업 대상 포함 금지.",
    "static_analysis": "정적 분석 산출물. 추출 바이너리는 .bin.disabled, 텍스트만 .txt.",
    "baseline_comparison": "공식 경로로 받은 정품과의 바이트 대조(출처·서명 기록 포함).",
    "persistence_review": "자동실행·로그온 스크립트·WMI·IFEO 점검. 비밀값 이름은 수집 제외.",
    "mitm_review": "프록시·인증서·hosts·DNS 점검.",
    "architecture_review": "감염 구조 도식·보고서(PDF/SVG) 생성물.",
    "admin_collect": "관리자 권한 읽기 전용 수집(SRUM·Prefetch·Amcache·BAM) 스크립트와 결과.",
    "analysis_tools": "pip --target 으로 벤더링한 OSS 툴체인(requirements-rea.txt 기준).",
    "evidence/scripts": "분석 스크립트. 모든 스크립트 docstring에 'never loads or executes sample code' 명시.",
}

README = """# {date}_{slug} — REA 케이스

- 담당: {agent} (1차) / 교차 검증: (예: Claude)
- 상태: 진행 중
- 규칙: 의심 파일 실행·복원·외부 업로드 금지 · 백신 예외 추가 금지 · 이동 전후 SHA-256 비교 · 설치/삭제/설정 변경은 승인 후

## 0. 결론
(확정된 사실만. 추정은 '추정'으로 표기)

## 1. 범위와 한계
| 본 것 | 못 본 것(이유) |
|---|---|

## 2. 감염/동작 구조
```mermaid
flowchart TD
  A[배포기] --> B[1단계 로더] --> C[2단계 로더] --> D[최종 페이로드]
```

## 3. 파일별 판정
| # | 파일 | 정체 | 판정 | 근거(파일·오프셋·스크립트) |
|---|---|---|---|---|

## 4. 시간순 재구성
| 시각 | 사건 | 출처 |
|---|---|---|

## 5. 증거 수준
| 주장 | 수준(직접 증거/정황/보류) | 근거 |
|---|---|---|

## 6. IOC
| 종류 | 값 |
|---|---|

## 7. 조치 · 다음 단계
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("slug")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--agent", default="Codex")
    a = ap.parse_args()

    case = Path(a.root) / f"{a.date}_{a.slug}"
    case.mkdir(parents=True, exist_ok=True)
    created = []
    for sub, note in STAGES.items():
        d = case / sub
        d.mkdir(parents=True, exist_ok=True)
        keep = d / "_PURPOSE.txt"
        if not keep.exists():
            keep.write_text(note + "\n", encoding="utf-8")
            created.append(str(keep.relative_to(case)))
    files = {
        "README.md": README.format(date=a.date, slug=a.slug, agent=a.agent),
        "case.json": json.dumps({
            "case": f"{a.date}_{a.slug}",
            "created": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "lead_agent": a.agent,
            "rules": ["no-execution", "hash-before-after", "approval-before-change", "no-av-exclusions"],
            "limitations": [],
        }, ensure_ascii=False, indent=2) + "\n",
        "suspect_hashes.json": "{}\n",
    }
    for name, text in files.items():
        p = case / name
        if not p.exists():
            p.write_text(text, encoding="utf-8")
            created.append(name)
    print(json.dumps({"case": str(case), "created": created}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
