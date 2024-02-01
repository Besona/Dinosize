import json
import random

def load_word_lists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def select_list(word_lists):
    while True:
        list_name = input("请输入要测试的列表编号：")
        full_list_name = 'list' + list_name
        if full_list_name in word_lists:
            return full_list_name, list_name
        else:
            print("列表不存在，请重新输入。")

def select_mode():
    while True:
        mode = input("请选择测试模式（1：中译英，2：英译中）：")
        if mode in ['1', '2']:
            return int(mode)
        else:
            print("输入错误，请重新输入。")

def test_words(word_list, mode, error_tracker):
    words = list(word_list.items())
    random.shuffle(words)
    wrong_words = []

    for i, (word, translation) in enumerate(words, start=1):
        if mode == 1:
            answer = input(f"{translation}: ")
            correct = answer.strip().lower() == word.lower()
        else:
            answer = input(f"{word}: ")
            correct = answer.strip() == translation

        if correct:
            print(f"正确！进度：{i}/{len(words)}")
        else:
            print(f"错误！正确答案是：{'英文' if mode == 1 else '中文'} - {word if mode == 1 else translation}")
            wrong_words.append((word, translation))
            error_tracker[word] += 1

    return wrong_words

def display_errors(list_number, round_count, error_tracker):
    print(f"\nlist{list_number}，第{round_count}轮的错误统计：")
    sorted_errors = sorted(error_tracker.items(), key=lambda item: item[1], reverse=True)
    for word, count in sorted_errors:
        if count > 0:
            print(f"{word} 错误 {count} 次")

def main():
    word_lists = load_word_lists("word_lists.json")
    full_list_name, list_number = select_list(word_lists)
    mode = select_mode()

    error_tracker = {word: 0 for word in word_lists[full_list_name].keys()}
    wrong_words = test_words(word_lists[full_list_name], mode, error_tracker)
    round_count = 1

    while wrong_words:
        print(f"\n第{round_count}轮测试结束。开始第{round_count + 1}轮测试错误的单词。")
        wrong_words = test_words(dict(wrong_words), mode, error_tracker)
        round_count += 1

    print("\n所有单词测试完毕！")
    display_errors(list_number, round_count - 1, error_tracker)

if __name__ == "__main__":
    main()
