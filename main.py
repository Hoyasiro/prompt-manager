CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

def get_default_prompts():
    return [
        {
            "title": "블로그 글 작성 도우미",
            "content": "당신은 10년 경력의 전문 블로거입니다. SEO에 최적화된 글을 작성해주세요.",
            "category": "텍스트 생성",
            "favorite": True,
        },
        {
            "title": "제품 썸네일 생성",
            "content": "정사각형 구도, 밝은 단색 배경, 부드러운 스튜디오 조명으로 썸네일을 만들어주세요.",
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "IT 컨설턴트 페르소나",
            "content": "당신은 15년 경력의 IT 컨설턴트입니다. 결론, 근거, 실행 계획 순서로 답변해주세요.",
            "category": "페르소나",
            "favorite": False,
        },
    ]
def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")

def main():
    prompts = get_default_prompts()

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("\n프로그램을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("\n해당 기능은 아직 준비 중입니다.")
if __name__ == "__main__":
    main()  