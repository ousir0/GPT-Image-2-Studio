#!/usr/bin/env python3
import argparse
import json
import pathlib
import textwrap
from datetime import datetime


DEFAULT_MODEL = "gpt-image-2"


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in textwrap.dedent(text).strip().splitlines()) + "\n"


def read_optional_file(path: str | None) -> str:
    if not path:
        return ""
    return pathlib.Path(path).expanduser().resolve().read_text(encoding="utf-8").strip()


def base_context(args: argparse.Namespace) -> str:
    facts = read_optional_file(args.facts_file)
    parts = [
        f"用户简报：{args.brief}",
        f"目标受众：{args.audience}",
        f"输出语言：{args.language}",
        f"期望风格：{args.style}",
    ]
    if args.reference_note:
        parts.append(f"参考图/素材说明：{args.reference_note}")
    if facts:
        parts.append(f"可用事实材料：\n{facts}")
    return "\n".join(parts)


def prompt_frame(title: str, body: str, args: argparse.Namespace) -> str:
    return clean(
        f"""
        {title}

        {base_context(args)}

        生成要求：
        {body}

        通用约束：
        - 使用 {args.language} 作为图中文字语言，关键标题和标签必须清晰可读。
        - 画面必须像可以直接交付的设计稿，不要像随机 AI 试验图。
        - 避免水印、乱码、无意义小字、脏乱边缘、过度装饰。
        - 如果需要后续放入 PPT 或文章，请保留足够安全边距和留白。
        """
    )


def ppt_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "ppt-cover",
            "PPT 封面主视觉",
            """
            - 生成一张 16:9 横版 PPT 封面 hero 图。
            - 画面要能表达整个主题的核心隐喻。
            - 在左上或中左区域保留标题安全区，不要把小字塞满。
            - 主视觉集中、层次清晰，适合商务汇报或方案提案。
            - 不要生成完整 PPT 页面，只生成可作为封面背景的高质量视觉图。
            """,
        ),
        (
            "ppt-section-opener",
            "PPT 章节页背景",
            """
            - 生成一张 16:9 章节分隔页视觉图。
            - 用一个明确场景或符号表达“从问题到解决方案”的转折。
            - 画面右侧或底部要有大面积留白，方便后续叠加章节标题。
            - 与封面保持统一色板、统一材质和统一设计气质。
            """,
        ),
        (
            "ppt-process",
            "PPT 流程图视觉",
            """
            - 生成一张适合放入 PPT 的流程图式视觉图。
            - 结构包含 4 个阶段：现状洞察、关键问题、解决路径、预期结果。
            - 使用模块、箭头、编号、图标和简短标签表达，不要写长段落。
            - 信息密度中等，重点是清楚、好读、专业。
            """,
        ),
        (
            "ppt-data-story",
            "PPT 数据故事图",
            """
            - 生成一张数据故事型插图，不需要真实数字时可用抽象数据形态。
            - 包含一个主数据图形、2-3 个要点 callout、一个结论区。
            - 风格要像咨询公司或科技公司方案页里的高级配图。
            - 不要做成普通柱状图截图，要有视觉叙事感。
            """,
        ),
        (
            "ppt-scenario",
            "PPT 场景落地图",
            """
            - 生成一张“方案落地后的使用场景”视觉图。
            - 展示人物、产品、空间或工作流如何在真实环境中发生作用。
            - 要有明确前景主体、中景动作、背景环境。
            - 适合作为案例页、客户价值页或落地场景页配图。
            """,
        ),
        (
            "ppt-closing",
            "PPT 结尾愿景图",
            """
            - 生成一张用于结尾页的愿景型视觉。
            - 情绪应更开放、更有未来感，但不要空泛。
            - 画面要能承载一句总结性大标题，保留干净留白。
            - 与整套视觉保持一致。
            """,
        ),
    ]
    return build_items(prompts, args)


def infographic_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "infographic-long-card",
            "竖版信息图 / 长图",
            """
            - 生成一张高质量竖版信息图，适合公众号、小红书或方案附录。
            - 结构分为：标题区、核心结论、3-5 个知识模块、图解主视觉、总结区。
            - 使用圆角模块、局部放大、标注箭头、短标签、评分卡或 Top 5 模块。
            - 如果有事实材料，优先使用事实材料；没有事实材料时，只做概念性表达，不编造具体数字。
            - 视觉参考：高级博物图鉴、现代百科书页、社交媒体收藏卡。
            """,
        )
    ]
    return build_items(prompts, args)


def comic_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "comic-character-bible",
            "漫画角色设定卡",
            """
            - 生成一张角色设定卡，用于后续漫画保持一致性。
            - 包含主角全身图、3 个表情小头像、服装细节、关键道具、简短身份信息。
            - 文字标签简洁，角色外观必须明确、可复用。
            - 画风适合后续生成多格漫画。
            """,
        ),
        (
            "comic-page-01",
            "漫画第一页 / 试制分镜",
            """
            - 生成一页 6 格漫画，从上到下阅读。
            - 每格都要有清晰镜头动作，角色外观与角色设定卡保持一致。
            - 对白必须短，中文气泡清晰可读。
            - 页面要有开端、冲突、转折和结尾钩子。
            - 不要让文字挤满画面，优先用动作和表情讲故事。
            """,
        ),
    ]
    return build_items(prompts, args)


def ui_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "ui-concept-board",
            "产品 UI 概念板",
            """
            - 生成一张 UI 设计概念板，展示一个完整产品界面系统。
            - 包含首页或仪表盘主屏、2-3 个功能卡片、导航栏、关键 CTA、状态组件。
            - 文字要像真实产品，不要随机乱码。
            - 视觉要像可放进产品方案 PPT 的高完成度设计稿。
            """,
        )
    ]
    return build_items(prompts, args)


def poster_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "poster-key-visual",
            "海报 / Banner 主视觉",
            """
            - 生成一张高完成度商业海报主视觉。
            - 包含清晰主体、标题区、卖点标签区、行动号召区。
            - 标题文案可根据用户简报提炼，但不要编造真实品牌背书。
            - 适合活动推广、电商主图、品牌 KV 或社媒封面。
            """,
        )
    ]
    return build_items(prompts, args)


def article_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "article-hero",
            "文章头图",
            """
            - 生成一张文章头图，用于表达主题核心冲突或核心观点。
            - 画面要有强识别度，适合公众号、网站或小红书封面。
            - 保留标题安全区，不要生成太多正文小字。
            """,
        ),
        (
            "article-inline-01",
            "文章正文配图 1",
            """
            - 生成一张正文插图，解释主题中的第一个关键概念。
            - 风格与头图一致，但构图更简洁，更适合插入段落之间。
            """,
        ),
        (
            "article-summary-card",
            "文章总结卡",
            """
            - 生成一张结尾总结卡，包含 3-5 个简短要点。
            - 结构清晰，适合读者收藏或转发。
            """,
        ),
    ]
    return build_items(prompts, args)


def game_pack(args: argparse.Namespace) -> list[dict]:
    prompts = [
        (
            "game-world-keyart",
            "游戏世界观主视觉",
            """
            - 生成一张游戏世界观 key art。
            - 包含主场景、核心角色剪影、世界观符号和气氛光。
            - 画面要能让人一眼判断游戏类型和情绪。
            """,
        ),
        (
            "game-ui-status",
            "游戏 UI 状态页",
            """
            - 生成一张游戏角色状态页 UI。
            - 包含角色立绘、属性栏、技能卡、装备槽、地图或任务信息。
            - 信息量丰富但层级清楚，文字标签清晰。
            """,
        ),
    ]
    return build_items(prompts, args)


SCENE_BUILDERS = {
    "ppt": ppt_pack,
    "infographic": infographic_pack,
    "comic": comic_pack,
    "ui": ui_pack,
    "poster": poster_pack,
    "article": article_pack,
    "game": game_pack,
}


def build_items(prompt_specs: list[tuple[str, str, str]], args: argparse.Namespace) -> list[dict]:
    items = []
    for index, (item_id, title, body) in enumerate(prompt_specs, start=1):
        items.append(
            {
                "id": item_id,
                "title": title,
                "mode": "generate",
                "model": args.model,
                "n": args.n,
                "response_format": args.response_format,
                "prompt": prompt_frame(title, body, args),
                "order": index,
            }
        )
    return items


def write_pack(args: argparse.Namespace) -> pathlib.Path:
    outdir = pathlib.Path(args.out).expanduser().resolve()
    prompts_dir = outdir / "prompts"
    outputs_dir = outdir / "outputs"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    items = SCENE_BUILDERS[args.scene](args)
    manifest_items = []

    for item in items:
        prompt_path = prompts_dir / f"{item['order']:02d}-{item['id']}.txt"
        prompt_path.write_text(item.pop("prompt"), encoding="utf-8")
        manifest_items.append(
            {
                **item,
                "prompt_file": str(prompt_path),
                "outdir": str(outputs_dir / item["id"]),
            }
        )

    manifest = {
        "version": 1,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "scene": args.scene,
        "brief": args.brief,
        "style": args.style,
        "audience": args.audience,
        "language": args.language,
        "items": manifest_items,
    }
    manifest_path = outdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    plan_lines = [
        f"# GPT Image 2 Prompt Pack: {args.scene}",
        "",
        f"- Brief: {args.brief}",
        f"- Style: {args.style}",
        f"- Audience: {args.audience}",
        f"- Language: {args.language}",
        "",
        "## Items",
        "",
    ]
    for item in manifest_items:
        plan_lines.append(f"- `{item['id']}`: {item['title']} -> `{item['prompt_file']}`")
    (outdir / "package-plan.md").write_text("\n".join(plan_lines) + "\n", encoding="utf-8")
    return manifest_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a scene-specific gpt-image-2 prompt pack.")
    parser.add_argument("--scene", required=True, choices=sorted(SCENE_BUILDERS), help="Prompt pack scene")
    parser.add_argument("--brief", required=True, help="User brief or topic")
    parser.add_argument("--style", default="高级、清晰、可交付、适合商业使用", help="Visual style")
    parser.add_argument("--audience", default="普通用户和业务决策者", help="Target audience")
    parser.add_argument("--language", default="简体中文", help="In-image language")
    parser.add_argument("--facts-file", help="Optional text file with verified facts or source notes")
    parser.add_argument("--reference-note", help="Optional note about reference images")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model")
    parser.add_argument("--n", type=int, default=1, choices=range(1, 5), help="Images per prompt")
    parser.add_argument("--response-format", default="b64_json", choices=["b64_json", "url"])
    parser.add_argument("--out", required=True, help="Output prompt pack directory")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    manifest_path = write_pack(args)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
