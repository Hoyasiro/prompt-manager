CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

def get_default_prompts():
    return [
        {
            "title": "불만 이메일 답변초안 작성",
            "content": """[역할과 목표] 너는 기업 담당자를 대신해 고객 불만 이메일 답변 초안을 작성하는 전문 라이터다. 고객의 불만을 항목별로 파악하고, 입력된 조건에 맞는 공식 답변 초안을 생성하는 것이 목표다. [답변 형식]- 출력 구조: 제목 / 도입부 / 불만 항목별 답변(번호 유지, 불만 메일에 numbering이 없다면 순서대로 번호 붙이) / 마무리 / 서명란- 불만 항목이 여러 개일 경우 반드시 번호를 유지하여 각각 답변한다.- 서명란은 [이름], [직책], [연락처] 형태의 빈칸으로 출력한다.[안전장치]- 입력 정보가 부족하거나 답변 방향이 불명확하면 초안 작성 전에 먼저 질문한다.- 질문에 대한 답변이 단답형이어도 문맥에 맞춰서 이해해야 한다.- 질문에 대한 답변을 받았음에도 불구하고 모호하거나 여러 의미의 중복 또는 상호 충돌되는 내용의 답변이 있다면, 되물을 수 있다.- 질문에 대한 답변이 '잘 모르겠다.'인 경우, "확인 후 안내" 문구로 처리한다.- 처리 가능 여부가 불확실한 요청(예: 환불 가능 여부)은 임의로 확정하지 않고 "확인 후 안내" 문구로 처리한다.- 답변 작성이 불가능한 항목이 있으면 불가능하다고 명시한다.[숫자·사실 규칙]- 원문에 없는 날짜, 금액, 이름, 정책 수치는 절대 지어내지 않는다.- 원문에 명시되지 않은 사실이 필요한 경우 반드시 '확인 필요' 또는 '[    ]'로 표시한다.- 애매한 표현(예: "빠른 시일 내")은 구체적 기한이 없을 경우 그대로 유지하되, 구체적 날짜가 필요한 자리는 '[날짜 확인 필요]'로 표시한다.""",
            "category": "텍스트 생성",
            "favorite": True,
        },
        {
            "title": "광고 이미지 생성",
            "content": "documentary photography, natural available light, 35mm lens, shallow depth of field, warm low-angle backlight, muted palette of black, orange, off-white, fine film grain, no text, no letters, no logo",
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "고교야구 투구수 매니저",
            "content": "너는 고교야구 투수 관리 담당자다. 감독에게 보낼 투구수 초과 위험 안내 메시지를 한국어로 3문장 이내로 작성한다.",
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

def show_by_category(prompts):
    print("\n=== 카테고리별 조회 ===")
    category = choose_category()

    found = [(number, prompt)
             for number, prompt in enumerate(prompts, start=1)
             if prompt["category"] == category]

    if not found:
        print(f"\n[{category}] 카테고리에 등록된 프롬프트가 없습니다.")
        return

    print(f"\n[{category}] 카테고리 프롬프트:")
    print_prompts(found)

def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = input_required("검색어: ").lower()

    found = [(number, prompt)
             for number, prompt in enumerate(prompts, start=1)
             if keyword in prompt["title"].lower()
             or keyword in prompt["content"].lower()]

    if not found:
        print(f"\n'{keyword}' 에 해당하는 프롬프트를 찾지 못했습니다.")
        return

    print("\n검색 결과:")
    print_prompts(found)

def show_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    raw = input("프롬프트 번호 입력: ").strip()

    if not raw.isdigit():
        print("   [!] 숫자로 된 번호를 입력해 주세요.")
        return

    index = int(raw) - 1
    if not 0 <= index < len(prompts):
        print("   [!] 존재하지 않는 번호입니다.")
        return

    prompt = prompts[index]
    print("\n" + "-" * 44)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '☆'}")
    print("-" * 44)
    print("내용:")
    print(prompt["content"])
    print("-" * 44)

def toggle_favorite(prompts):
    print("\n=== 즐겨찾기 관리 ===")
    raw = input("프롬프트 번호 입력: ").strip()

    if not raw.isdigit():
        print("   [!] 숫자로 된 번호를 입력해 주세요.")
        return

    index = int(raw) - 1
    if not 0 <= index < len(prompts):
        print("   [!] 존재하지 않는 번호입니다.")
        return

    prompt = prompts[index]
    prompt["favorite"] = not prompt["favorite"]

    if prompt["favorite"]:
        print(f"\n'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다! ⭐")
    else:
        print(f"\n'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    found = [(number, prompt)
             for number, prompt in enumerate(prompts, start=1)
             if prompt["favorite"]]

    if not found:
        print("즐겨찾기한 프롬프트가 없습니다. 6번 메뉴에서 등록해 보세요.")
        return

    print_prompts(found, unit="즐겨찾기")

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

        elif choice == "3":
            show_by_category(prompts)

        elif choice == "4":
            search_prompt(prompts)

        elif choice == "5":
            show_detail(prompts)

        elif choice == "6":
            toggle_favorite(prompts)

        elif choice == "7":
            show_favorites(prompts)

        else:
            print("\n[!] 0~7 사이의 번호만 입력할 수 있습니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()