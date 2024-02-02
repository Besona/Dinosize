import json
import random
import time

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
        else:  # 英译中模式
            print(word)
            input("按下Enter显示中文意思...")
            print(f"中文意思：{translation}")
            answer = input("是否做对了？(1: 正确, 0: 错误): ")
            correct = answer.strip() == '1'

        if correct:
            print(f"正确！进度：{i}/{len(words)}")
        else:
            print(f"错误！正确答案是：{'英文' if mode == 1 else '中文'} - {word if mode == 1 else translation}")
            wrong_words.append((word, translation))
            error_tracker[word] += 1

    return wrong_words

def display_errors(word_list, mode, list_number, round_count, error_tracker):
    print(f"\nlist{list_number}，第{round_count}轮的错误统计：")
    sorted_errors = sorted(error_tracker.items(), key=lambda item: item[1], reverse=True)
    for word, count in sorted_errors:
        if count > 0:
            if mode == 1:  # 中译英
                print(f"{word_list[word]} - {word} 错误 {count} 次")
            else:  # 英译中
                print(f"{word} - {word_list[word]} 错误 {count} 次")

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒 "

def main():
    word_lists = load_word_lists("word_lists.json")
    full_list_name, list_number = select_list(word_lists)
    mode = select_mode()

    start_time = time.time()  # 开始计时

    word_list = word_lists[full_list_name]
    error_tracker = {word: 0 for word in word_list.keys()}
    wrong_words = test_words(word_list, mode, error_tracker)
    round_count = 1

    while wrong_words:
        print(f"\n第{round_count}轮测试结束。开始第{round_count + 1}轮测试错误的单词。")
        wrong_words = test_words(dict(wrong_words), mode, error_tracker)
        round_count += 1

    end_time = time.time()  # 结束计时
    total_time = end_time - start_time  # 计算总用时

    print("\n所有单词测试完毕！")
    display_errors(word_list, mode, list_number, round_count - 1, error_tracker)
    print(f"\n本组单词测试用时：{format_time(total_time)}")

if __name__ == "__main__":
    main()
