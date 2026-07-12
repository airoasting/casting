#!/usr/bin/env python3
"""디자인본부 역할이 실제 이미지를 산출하는 도구.

흐름: gpt-image 스킬(있으면)으로 한국어 요청을 7원칙 이미지 프롬프트로 다듬은 뒤,
그 프롬프트를 이 스크립트로 OpenAI 이미지 API(gpt-image-1)에 넘겨 PNG를 만든다.
키가 없으면 완성된 프롬프트만 산출물로 제시하고 그 사실을 밝힌다(정직한 폴백).

사용:
  OPENAI_API_KEY=... python scripts/gen_image.py "<프롬프트>" out.png [--size 1024x1024] [--quality high]

산출물 유형별 권장 비율:
  슬라이드 1536x1024 · 카드뉴스 1024x1024 · 인포그래픽 1024x1536 · 브랜드/썸네일 1024x1024
의존: pip install openai (v1+). gpt-image-1은 b64_json으로 반환한다.
"""
import os
import sys
import base64
import argparse


def main():
    ap = argparse.ArgumentParser(description="OpenAI gpt-image-1로 이미지 생성")
    ap.add_argument("prompt", help="완성된 이미지 프롬프트")
    ap.add_argument("outfile", help="저장할 PNG 경로")
    ap.add_argument("--size", default="1024x1024",
                    help="1024x1024 | 1536x1024 | 1024x1536")
    ap.add_argument("--quality", default="high", help="low | medium | high")
    args = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY가 없습니다. 키를 설정하거나, 완성된 프롬프트를 "
                 "산출물로 제시하고 '이미지 미생성(프롬프트만)'임을 밝히세요.")
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("openai 패키지가 필요합니다: pip install openai")

    client = OpenAI(api_key=key)
    res = client.images.generate(
        model="gpt-image-1",
        prompt=args.prompt,
        size=args.size,
        quality=args.quality,
        n=1,
    )
    with open(args.outfile, "wb") as f:
        f.write(base64.b64decode(res.data[0].b64_json))
    print(f"saved {args.outfile}")


if __name__ == "__main__":
    main()
