# backend/utils/report_generator.py
import os

try:
    from openai import OpenAI
    _OPENAI_OK = True
except Exception:
    _OPENAI_OK = False

SOURCE_MAP = {
    "PP": "常见于包装薄膜、瓶盖、纺织纤维及一次性容器，其在使用及废弃处理过程中易因机械破碎和摩擦而释放。",
    "PS": "主要存在于泡沫塑料制品（如食品包装、保温材料）及实验室耗材，因其脆性高，在物理扰动下易形成颗粒。",
    "PE": "广泛用于购物袋、薄膜及瓶体，环境老化及紫外光照射可促进其裂解为微塑料。", 
    "PET": "主要来源于饮料瓶及纺织纤维（涤纶），衣物洗涤是其重要释放途径。",
    "PVC": "常见于管材、电缆护套及建筑材料，在长期磨损与老化过程中可释放颗粒。",
    "PA": "应用于尼龙纤维、渔网及工业绳索，因摩擦与机械磨损易脱落微纤维。"
}

RISK_GENERAL = (
    "微塑料可作为环境中污染物和添加剂的载体进入生物体，其在生理系统中的累积可能引发氧化应激、炎症反应及细胞损伤等效应。"
    "当前关于其对人体健康的长期影响尚存在不确定性，但其潜在风险已引起广泛关注。"
)

SUGGESTIONS_BASE = [
    "加强检测环节质量控制，避免采样、制备和分析过程中的二次污染。",
    "减少一次性塑料制品的使用，推广可降解或可回收替代材料。",
    "建立完善的分类回收与处理机制，降低微塑料经由城市污水和废弃物流入环境的概率。",
    "在科研与监测实验中使用低脱落耗材，并设置空白对照以保证数据可靠性。"
]

EXTRA_ADVICE = {
    "PP": "针对 PP：应重点关注包装和纺织环节，其在使用及废弃过程中可能成为重要释放源。",
    "PS": "针对 PS：应控制发泡聚苯乙烯制品的应用与流通，以减少因破碎和热处理导致的二次释放。"
}

def _format_counts(counts: dict) -> str:
    total = sum(counts.values()) or 0
    parts = [f"{k}：{v} 颗" for k, v in counts.items()]
    return f"本次检测共检出微塑料颗粒 {total} 颗，其中 " + "，".join(parts) + "。"

def _template_conclusion(counts: dict) -> str:
    if not counts:
        return "未在图像中检出明确的微塑料颗粒，可能与图像质量或样本浓度偏低有关。"

    total = sum(counts.values())
    allowed = list(counts.keys())
    top_cls, top_cnt = max(counts.items(), key=lambda x: x[1])
    top_ratio = (top_cnt / total) if total else 0

    lines = []
    lines.append(_format_counts(counts))

    if len(allowed) == 1:
        lines.append(f"颗粒组成以 {top_cls} 为主，占比约 {top_ratio:.0%}。")
    else:
        compo = "、".join(allowed)
        lines.append(f"检测结果显示颗粒组成包含 {compo}，其中 {top_cls} 占比最高（约 {top_ratio:.0%}）。")

    srcs = [f"{k}：{SOURCE_MAP.get(k)}" for k in allowed if k in SOURCE_MAP]
    lines.append("可能来源包括：\n- " + "\n- ".join(srcs))

    lines.append("潜在环境与健康风险：\n- " + RISK_GENERAL)

    adv = SUGGESTIONS_BASE.copy()
    for k in allowed:
        if k in EXTRA_ADVICE:
            adv.append(EXTRA_ADVICE[k])
    lines.append("建议措施：\n- " + "\n- ".join(adv))

    return "\n".join(lines)

def _gpt_polish(counts: dict, draft: str) -> str:
    if not _OPENAI_OK:
        return draft
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return draft

    try:
        client = OpenAI(api_key=api_key)
        allowed = ", ".join(counts.keys())
        total = sum(counts.values())
        prompt = (
            "你是一名科研助理。请基于以下检测摘要，生成一段正式的学术报告结论，"
            "保持结构完整（检出结果 → 成分比例 → 来源分析 → 潜在风险 → 建议措施），"
            f"仅限讨论以下类别：[{allowed}]，总颗粒数为 {total}。"
            "不得引入未检出的类别，也不得改变数值。保持学术、客观、中性语气。\n\n"
            f"【检测摘要】\n{draft}\n"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": "你是一名环境科学研究助理，负责撰写学术报告结论。"},
                {"role": "user", "content": prompt},
            ],
            timeout=30,
        )
        return resp.choices[0].message.content.strip() or draft
    except Exception:
        return draft

def generate_conclusion(counts: dict) -> str:
    draft = _template_conclusion(counts)
    polished = _gpt_polish(counts, draft)
    return polished