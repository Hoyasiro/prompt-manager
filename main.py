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

def input_required(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print(" [!] 값이 비어 있습니다. 다시 입력해 주세요.")

def choose_category():
    print("\n카테고리 선택:")
    for number, name in enumerate(CATEGORIES, start=1):
        print(f" {number}. {name}")
    print(f" {len(CATEGORIES) + 1}. 직접 입력")

    choice = input("선택: ").strip()
    if choice.isdigit():
        number = int(choice)
        if 1 <= number <= len(CATEGORIES):
            return CATEGORIES[number - 1]
        if number == len(CATEGORIES) + 1:
            return input_required("카테고리 직접 입력: ")
    print(" [!] 잘못된 선택입니다. '기타'로 저장합니다.")
    return "기타"


def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = input_required("제목: ")
    content = input_required("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    })
    print(f"\n'{title}' 프롬프트가 추가되었습니다! (총 {len(prompts)}개)")

def print_prompts(found, unit="프롬프트"):
    for number, prompt in found:
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")
    print(f"\n총 {len(found)}개의 {unit}")


def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 1번 메뉴로 먼저 추가해 주세요.")
        return
    print_prompts(list(enumerate(prompts, start=1)))

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

        elif choice == "1":
            add_prompt(prompts)

        elif choice == "2":
            show_list(prompts)

        else:
            print("\n[!] 0~7 사이의 번호만 입력할 수 있습니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()