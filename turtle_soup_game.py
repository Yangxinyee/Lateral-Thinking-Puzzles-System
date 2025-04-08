from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPNENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 全局初始化 client
client = OpenAI(api_key=OPNENAI_API_KEY)
# 谜面和真相
PUZZLE = """一个男人走进一家餐厅，点了一碗海龟汤。吃了一口后，他走出餐厅开枪自杀了。为什么？"""
TRUTH = """这个男人曾经在一次船难中获救。当时他和他的朋友以及一些幸存者漂流到一座荒岛上。
            岛上缺乏食物，如果再不吃东西的话就无法支撑到救援的到来。
            救援到来前，他的朋友给他端来一碗"海龟汤"，并告诉男人说是他们捕到的海龟做的。男人虽然觉得味道奇怪，但还是吃了。
            之后救援到来了，男人得救了，但是朋友却失踪了。
            多年后，他偶然在一家餐厅再次点了一碗真正的海龟汤，发现味道完全不同。
            他这才意识到，自己当年在岛上吃的根本不是海龟肉。
            原来当年男人的朋友为了救他，偷偷把自己的肉割下来煮成所谓的"海龟汤"给男人吃。
            面对这个可怕的真相，他无法承受，感到十分悲伤，于是自杀了。"""

# 🧠 使用新版接口调用 ChatGPT
def analyze_story_structure(puzzle, truth):
    system_prompt = (
        "你是一个专业的故事分析师，擅长从多个维度拆解故事结构。\n"
        "请从以下维度分析这个故事：\n"
        "1. 时间线：按时间顺序列出关键事件\n"
        "2. 因果关系：列出事件之间的因果关系链\n"
        "3. 人物动机：分析主要人物的心理动机\n"
        "4. 关键转折：指出故事中的关键转折点\n"
        "5. 隐藏线索：列出故事中隐藏的重要线索\n"
        "6. 情感发展：描述人物情感的变化过程\n"
        "请用JSON格式输出分析结果，包含以上所有维度。\n"
        "每个维度都要详细列出具体内容。"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"谜题：{puzzle}\n真相：{truth}"}
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content.strip()

def answer_question_with_llm(puzzle, truth, question, story_analysis, conversation_history=None):
    if conversation_history is None:
        conversation_history = []
    
    # 构建对话历史
    history_text = ""
    if conversation_history:
        history_text = "以下是之前的对话历史：\n"
        for i, (q, a) in enumerate(conversation_history, 1):
            history_text += f"{i}. 玩家：{q}\n   主持人：{a}\n"
    
    system_prompt = (
        "你是一个专业、幽默、富有同理心的海龟汤游戏主持人。\n"
        "你的目标是引导玩家通过提问和推理逐步接近真相，而不是直接揭示答案。\n"
        "谜题：" + puzzle + "\n"
        "真相：" + truth + "\n"
        "以下是故事的结构分析，请严格参考这些信息来引导玩家：\n"
        f"{story_analysis}\n"
        "以下是之前的对话历史，请严格参考这些信息来引导玩家：\n"
        f"{history_text}\n"
        "请遵循以下规则：\n"
        "1. 合理推理：回答'是'\n"
        "2. 偏离或无关：回答'否'\n"
        "3. 保持神秘：用最简短的回答，适当使用表情符号\n"
        "4. 避免矛盾：检查对话历史，确保回答一致性\n"
        "5. 处理矛盾：指出矛盾但不透露真相\n"
        "6. 保持连贯：基于历史回答保持一致性\n"
        "7. 不要自己推理，严格基于故事本身和故事结构分析以及对话历史来回答\n"
        "8. 如果根据历史对话和当前对话，你认为用户已经完成了整个推理过程，请告诉用户'你已经非常接近真相了，请把你的所有想法整理一下，然后告诉我'"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"用户提问：{question}，你的回答是："}
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content.strip()


def check_if_game_should_end(puzzle, truth, user_input, story_analysis, history_text):
    system_prompt = (
        "你是一个严格但公平的海龟汤游戏裁判。\n"
        "你的职责是判断玩家是否完全破解了谜题。\n"
        "之后会给故事的结构分析，用户的对话历史和用户的当前输入，请参考这些信息来判断玩家的回答：\n"
        "判断标准：\n"
        "1. 玩家必须完整描述事件发生的背景\n"
        "2. 玩家必须准确描述关键因果链\n"
        "3. 玩家必须说明人物的动机\n"
        "4. 玩家必须提到最终结局\n"
        "5. 如果玩家只说出部分真相，不能算作破解\n"
        "6. 如果玩家使用不同的表述方式但表达了相同的意思，可以算作正确\n"
        "7. 如果玩家在推理过程中提到了一些无关的细节，只要核心要素正确，可以算作破解\n"
        "请根据以上标准判断，只回答'是'或'否'。\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"玩家发言：{user_input}\n"
             f"故事结构分析：{story_analysis}\n"
             f"对话历史：{history_text}\n"
             f"请根据以上信息判断玩家是否破解了谜题："}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# 命令行交互
def main():
    print("欢迎来到海龟汤游戏！输入 q 退出。")
    print(f"谜面：{PUZZLE}")
    
    # 分析故事结构
    story_analysis = analyze_story_structure(PUZZLE, TRUTH)
    print("游戏开始！")
    print(story_analysis)
    # 初始化对话历史
    conversation_history = []

    while True:
        user_input = input("你的提问或推理：")
        if user_input.lower() in {"q", "quit", "exit"}:
            print("游戏结束，再见！")
            break

        response = answer_question_with_llm(PUZZLE, TRUTH, user_input, story_analysis, conversation_history)
        print(f"主持人：{response}")
        
        # 更新对话历史
        conversation_history.append((user_input, response))
        
        if check_if_game_should_end(PUZZLE, TRUTH, user_input, story_analysis, conversation_history) == "是":
            print("游戏结束，你成功破解了这个谜题！")
            print(f"真相：{TRUTH}")
            break

if __name__ == "__main__":
    main()
    