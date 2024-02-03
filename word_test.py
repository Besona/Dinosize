import json
import random
import time

def load_word_lists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def select_list(word_lists):
    while True:
        list_name = input("请输入要测试的列表编号：")
        if list_name == "114514":
            return "easter_egg", "彩蛋模式"
        full_list_name = 'list' + list_name
        if full_list_name in word_lists:
            return full_list_name, list_name
        else:
            print("列表不存在，请重新输入。")

def get_easter_egg_words(word_lists, A):
    all_words = [item for sublist in word_lists.values() for item in sublist.items()]
    return random.sample(all_words, min(A, len(all_words)))

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
        while True:
            if mode == 1:
                answer = input(f"{translation}: ")
                if answer.strip() == '1':
                    print(f"提示：本单词有 {len(word)} 个字母。")
                    continue
                elif answer.strip() == '2':
                    print(f"提示：本单词的首字母是 '{word[0]}'.")
                    continue
                correct = answer.strip().lower() == word.lower()
            else:  # 英译中模式
                print(word)
                input("按下Enter显示中文意思...")
                print(f"中文意思：{translation}")
                answer = input("是否做对了？(1: 正确, 0: 错误): ")
                correct = answer.strip() == '1'

            if correct:
                print(f"正确！进度：{i}/{len(words)}")
                break
            else:
                print(f"错误！正确答案是：{'英文' if mode == 1 else '中文'} - {word if mode == 1 else translation}")
                wrong_words.append((word, translation))
                error_tracker[word] += 1
                break

    return wrong_words


def display_errors(word_list, mode, list_number, round_count, error_tracker):
    if list_number == "彩蛋模式":
        list_info = "彩蛋模式"
    else:
        list_info = f"list{list_number}"
    print(f"\n{list_info}，第{round_count}轮的错误统计：")
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
    return f"{int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒"

def main():
    word_lists = load_word_lists("word_lists.json")
    full_list_name, list_number = select_list(word_lists)

    if full_list_name == "easter_egg":
        A = int(input("请输入彩蛋模式下要测试的单词数量："))
        word_list = dict(get_easter_egg_words(word_lists, A))
    else:
        word_list = word_lists[full_list_name]

    mode = select_mode()
    error_tracker = {word: 0 for word in word_list.keys()}
    start_time = time.time()
    wrong_words = test_words(word_list, mode, error_tracker)
    round_count = 1

    while wrong_words:
        print(f"\n第{round_count}轮测试结束。开始第{round_count + 1}轮测试错误的单词。")
        wrong_words = test_words(dict(wrong_words), mode, error_tracker)
        round_count += 1

    end_time = time.time()
    total_time = end_time - start_time
    print("\n所有单词测试完毕！")
    display_errors(word_list, mode, list_number, round_count - 1, error_tracker)
    print(f"\n本组单词测试用时：{format_time(total_time)}")

if __name__ == "__main__":
    main()
