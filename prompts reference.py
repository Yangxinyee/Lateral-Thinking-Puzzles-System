DEBATER = {
    "initial_answer_prompt_with_context": """Please review the following details:
Question: {QUESTION}
Context: {CONTEXT}
Agent {AGENT}, please generate your INITIAL ANSWER in the following format:
answer: {ANSWER}""",
    
    "initial_answer_prompt_without_context": """Please review the following detail:
Question: {QUESTION}
Agent {AGENT}, please generate your INITIAL ANSWER in the following format:
answer: {ANSWER}""",
    
    "debate_response_full_history": """Please review the full conversation history below:
{full_history}
Now, Agent {name}, considering your previous answer "{own_answer}" and your opponent's answer "{opponent_answer}" in Round {round_num}, please generate your NEXT RESPONSE in the format:
<argument>{your response}</argument>""",
    
    "debate_response_last_round": """Please review the most recent round of conversation below:
{last_round}
Now, Agent {name}, considering your previous answer "{own_answer}" and your opponent's answer "{opponent_answer}" in Round {round_num}, please generate your NEXT RESPONSE in the format:
<argument>{your response}</argument>""",
    
    "debater_ch_instru": """Your task is to critically examine your opponent’s answer, identify inconsistencies, logical errors, and unsupported assumptions, and ask probing questions that require clarification.""",
    
    "debater_de_instru": """Your role is to defend your original answer. Restate your main argument clearly, then address any challenges with detailed reasoning and evidence.""",
    
    "debater_sym_instru": """You are required to both defend your own answer and critically challenge your opponent’s answer. Identify any inconsistencies and improve your answer accordingly.""",
    
    "first_round_thinking": """1. Consider what extra context the judge needs to understand your argument.
2. Think step by step to plan a strong argument.
3. Include supporting evidence or quotes from the provided context.""",
    
    "second_round_thinking": """1. Identify the biggest flaws in your opponent's argument.
2. Critically evaluate and articulate these issues step by step.
3. Provide supporting evidence or quotes that refute your opponent's points.""",
    
    "nth_round_thinking": """1. Review the critiques your opponent has made.
2. Construct your counterargument in a step-by-step manner.
3. Include specific evidence or quotes to refute these critiques.""",
    
    "opening_argument_request": """Now it's your turn to construct your opening argument for why the answer to the question "{QUESTION}" is "{ANSWER_DEFENDING}"."""
}

JUDGE = {
    "judge_sym_instru": """Review the entire debate transcript below and synthesize the arguments from both agents. Determine which points are the most logically sound and well-supported, and then generate a concise final decision.""",
    
    "judge_asym_instru": """Review the entire debate transcript below and objectively synthesize the arguments from both agents. Evaluate which points are most logically sound and well-supported, then generate a concise final decision.""",
    
    "final_decision_prompt": """Based on the above transcript, please generate your FINAL DECISION, which answer do you support, if it is a year, give the answer in 4 digit number.
Your response must end with a line in the exact format:
final answer: YYYY"""
}