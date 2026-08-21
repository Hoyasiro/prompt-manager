import json
import os

DATA_FILE = "prompts.json"

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

def get_default_prompts():
    return [
        {
            "title": "불만 이메일 답변초안 작성",
            "content": """[역할과 목표] 너는 기업 담당자를 대신해 고객 불만 이메일 답변 초안을 작성하는 전문 라이터다. 고객의 불만을 항목별로 파악하고, 입력된 조건에 맞는 공식 답변 초안을 생성하는 것이 목표다. [답변 형식]- 출력 구조: 제목 / 도입부 / 불만 항목별 답변(번호 유지, 불만 메일에 numbering이 없다면 순서대로 번호 붙이) / 마무리 / 서명란- 불만 항목이 여러 개일 경우 반드시 번호를 유지하여 각각 답변한다.- 서명란은 [이름], [직책], [연락처] 형태의 빈칸으로 출력한다.[안전장치]- 입력 정보가 부족하거나 답변 방향이 불명확하면 초안 작성 전에 먼저 질문한다.- 질문에 대한 답변이 단답형이어도 문맥에 맞춰서 이해해야 한다.- 질문에 대한 답변을 받았음에도 불구하고 모호하거나 여러 의미의 중복 또는 상호 충돌되는 내용의 답변이 있다면, 되물을 수 있다.- 질문에 대한 답변이 '잘 모르겠다.'인 경우, "확인 후 안내" 문구로 처리한다.- 처리 가능 여부가 불확실한 요청(예: 환불 가능 여부)은 임의로 확정하지 않고 "확인 후 안내" 문구로 처리한다.- 답변 작성이 불가능한 항목이 있으면 불가능하다고 명시한다.[숫자·사실 규칙]- 원문에 없는 날짜, 금액, 이름, 정책 수치는 절대 지어내지 않는다.- 원문에 명시되지 않은 사실이 필요한 경우 반드시 '확인 필요' 또는 '[    ]'로 표시한다.\n- 애매한 표현(예: "빠른 시일 내")은 구체적 기한이 없을 경우 그대로 유지하되, 구체적 날짜가 필요한 자리는 '[날짜 확인 필요]'로 표시한다.""",
            "category": "텍스트 생성",
            "favorite": True,
            "views": 0,
        },
        {
            "title": "광고 이미지 생성",
            "content": "documentary photography, natural available light, 35mm lens, shallow depth of field, warm low-angle backlight, muted palette of black, orange, off-white, fine film grain, no text, no letters, no logo",
            "category": "이미지 생성",
            "favorite": False,
            "views": 0,
        },
        {
            "title": "고교야구 투구수 매니저",
            "content": "너는 고교야구 투수 관리 담당자다. 감독에게 보낼 투구수 초과 위험 안내 메시지를 한국어로 3문장 이내로 작성한다.",
            "category": "페르소나",
            "favorite": False,
            "views": 0,
        },
    ]

def save_prompts(prompts):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"   [!] 저장에 실패했습니다: {e}")


def load_prompts():
    if not os.path.exists(DATA_FILE):
        return get_default_prompts()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        for prompt in prompts:
            if "views" not in prompt:
                prompt["views"] = 0
        return prompts
    except Exception as e:
        print(f"   [!] 불러오기에 실패해 기본 데이터로 시작합니다: {e}")
        return get_default_prompts()

def export_markdown(prompts):
    print("\n=== Markdown 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    filename = "prompts.md"
    lines = ["# 나만의 프롬프트 모음\n"]

    for category in CATEGORIES:
        found = [p for p in prompts if p["category"] == category]
        if not found:
            continue

        lines.append(f"\n## {category}\n")
        for prompt in found:
            star = " ⭐" if prompt["favorite"] else ""
            lines.append(f"\n### {prompt['title']}{star}\n")
            lines.append(f"```\n{prompt['content']}\n```\n")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(lines))
        print(f"'{filename}' 파일로 내보냈습니다! (총 {len(prompts)}개)")
    except Exception as e:
        print(f"   [!] 내보내기에 실패했습니다: {e}")

def input_required(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print(" [!] 값이 비어 있습니다. 다시 입력해 주세요.")

def ask_prompt_index(prompts):
    raw = input("프롬프트 번호 입력: ").strip()

    if not raw.isdigit():
        print("   [!] 숫자로 된 번호를 입력해 주세요.")
        return None

    index = int(raw) - 1
    if not 0 <= index < len(prompts):
        print("   [!] 존재하지 않는 번호입니다.")
        return None

    return index

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
        "views": 0,
    })
    print(f"\n'{title}' 프롬프트가 추가되었습니다! (총 {len(prompts)}개)")
    save_prompts(prompts)

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
    prompt["views"] = prompt.get("views", 0) + 1
    save_prompts(prompts)

    print("\n" + "-" * 44)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '☆'}")
    print(f"조회수: {prompt['views']}회")
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
    save_prompts(prompts)

def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    found = [(number, prompt)
             for number, prompt in enumerate(prompts, start=1)
             if prompt["favorite"]]

    if not found:
        print("즐겨찾기한 프롬프트가 없습니다. 6번 메뉴에서 등록해 보세요.")
        return

    print_prompts(found, unit="즐겨찾기")

def show_top_viewed(prompts):
    print("\n=== 조회수 Top 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    ranked = sorted(enumerate(prompts, start=1),
                    key=lambda item: item[1].get("views", 0),
                    reverse=True)

    for rank, (number, prompt) in enumerate(ranked, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{rank}위. [{prompt['category']}] {prompt['title']}{star} "
              f"({prompt.get('views', 0)}회)")

    print(f"\n총 {len(prompts)}개의 프롬프트")

def edit_prompt(prompts):
    print("\n=== 프롬프트 수정 ===")
    index = ask_prompt_index(prompts)
    if index is None:
        return

    prompt = prompts[index]
    print(f"\n현재 제목: {prompt['title']}")
    print("(엔터만 누르면 기존 값을 유지합니다)")

    new_title = input("새 제목: ").strip()
    if new_title:
        prompt["title"] = new_title

    print(f"\n현재 내용: {prompt['content'][:40]}...")
    new_content = input("새 내용: ").strip()
    if new_content:
        prompt["content"] = new_content

    print(f"\n현재 카테고리: {prompt['category']}")
    answer = input("카테고리도 변경할까요? (y/n): ").strip().lower()
    if answer == "y":
        prompt["category"] = choose_category()

    save_prompts(prompts)
    print(f"\n'{prompt['title']}' 프롬프트를 수정했습니다!")


def delete_prompt(prompts):
    print("\n=== 프롬프트 삭제 ===")
    index = ask_prompt_index(prompts)
    if index is None:
        return

    title = prompts[index]["title"]
    answer = input(f"'{title}' 프롬프트를 정말 삭제할까요? (y/n): ").strip().lower()
    if answer != "y":
        print("삭제를 취소했습니다.")
        return

    del prompts[index]
    save_prompts(prompts)
    print(f"\n'{title}' 프롬프트를 삭제했습니다. (남은 {len(prompts)}개)")

def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. Markdown 내보내기")
    print("9. 조회수 Top 목록")
    print("10. 프롬프트 수정")
    print("11. 프롬프트 삭제")
    print("0. 종료")

def main():
    prompts = load_prompts()

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

        elif choice == "8":
            export_markdown(prompts)

        elif choice == "9":
            show_top_viewed(prompts)

        elif choice == "10":
            edit_prompt(prompts)

        elif choice == "11":
            delete_prompt(prompts)

        else:
            print("\n[!] 0~11 사이의 번호만 입력할 수 있습니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()