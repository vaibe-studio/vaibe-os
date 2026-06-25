"""Parser for vAIbe-media character sheets.

Extracts Prompt Anchors, style blocks, and reference image paths
from the character-sheets.md file.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


STYLE_BLOCK = (
    "Adult Swim cartoon style, thick black outlines, cel-shading, "
    "vibrant colors, expressive face, slightly exaggerated proportions, "
    "square crop, Telegram avatar format"
)

NEGATIVE_PROMPT = (
    "blurry, low quality, deformed, ugly, text, watermark, signature, "
    "bad anatomy, extra fingers, mutated hands, poorly drawn face, "
    "realistic photo, 3d render, photorealistic"
)

CHARACTER_SHEETS_PATH = Path(
    "Проекты/vAIbe-media/Задачи/008-Аватары для каналов vAIbe-media/results/v1/character-sheets.md"
)

REFERENCE_IMAGES_DIR = Path(
    "Проекты/vAIbe-media/Задачи/008-Аватары для каналов vAIbe-media/results/v1"
)


@dataclass
class Character:
    name_ru: str
    name_en: str
    role: str
    prompt_anchor: str
    colors: dict[str, str] = field(default_factory=dict)
    ref_front: Optional[str] = None
    ref_profile: Optional[str] = None
    ref_fullbody: Optional[str] = None


# Pre-defined character data extracted from character-sheets.md
CHARACTERS: dict[str, Character] = {
    "алекс байтов": Character(
        name_ru="Алекс Байтов",
        name_en="Alex Bytov",
        role="Технооптимист",
        prompt_anchor=(
            "Male character, angular jawline, high cheekbones, confident smirk, "
            "one eye slightly squinted, dark messy medium-length hair with subtle "
            "cyan-blue tint at the tips, lean build, slight programmer slouch, "
            "late 20s, thin line mark on temple"
        ),
        colors={"primary": "#00BCD4", "secondary": "#006064", "accent": "#76FF03"},
        ref_front="alex-bytov-ref-front.png",
        ref_profile="alex-bytov-ref-profile.png",
        ref_fullbody="alex-bytov-ref-fullbody.png",
    ),
    "марина народная": Character(
        name_ru="Марина Народная",
        name_en="Marina Narodnaya",
        role="Социал-прагматик",
        prompt_anchor=(
            "Female character, round soft face, warm expressive big brown eyes "
            "with slight wet shine, light smile lines around eyes, chestnut "
            "shoulder-length slightly wavy hair tucked behind one ear, average "
            "build, mid-30s to 40, small beauty mark near corner of mouth"
        ),
        colors={"primary": "#FF8F00", "secondary": "#880E4F", "accent": "#FFF8E1"},
        ref_front="marina-narodnaya-ref-front.png",
        ref_profile="marina-narodnaya-ref-profile.png",
        ref_fullbody="marina-narodnaya-ref-fullbody.png",
    ),
    "дмитрий коренев": Character(
        name_ru="Дмитрий Коренев",
        name_en="Dmitry Korenev",
        role="Традиционалист",
        prompt_anchor=(
            "Male character, elongated noble face, high forehead, thoughtful "
            "expression, deep-set gray-green attentive eyes, dark-blond hair "
            "with gray streaks swept back, short well-groomed beard with gray, "
            "medium build with upright dignified posture, early 50s, round "
            "reading glasses perched on tip of nose"
        ),
        colors={"primary": "#3E2723", "secondary": "#1B5E20", "accent": "#FFB300"},
        ref_front="dmitry-korenev-ref-front.png",
        ref_profile="dmitry-korenev-ref-profile.png",
        ref_fullbody="dmitry-korenev-ref-fullbody.png",
    ),
    "лика зелёная": Character(
        name_ru="Лика Зелёная",
        name_en="Lika Zelenaya",
        role="Экопрогрессист",
        prompt_anchor=(
            "Young female character, sharp lively face, wide cheeky grin with "
            "dimples, bright green eyes wide open with defiant look, short "
            "asymmetric bob haircut one side longer, dark hair with bright "
            "green-dyed tips, thin energetic build, early 20s, small green "
            "nose stud piercing"
        ),
        colors={"primary": "#4CAF50", "secondary": "#BF360C", "accent": "#FF7043"},
        ref_front="lika-zelenaya-ref-front.png",
        ref_profile="lika-zelenaya-ref-profile.png",
        ref_fullbody="lika-zelenaya-ref-fullbody.png",
    ),
    "игорь державин": Character(
        name_ru="Игорь Державин",
        name_en="Igor Derzhavin",
        role="Державник",
        prompt_anchor=(
            "Male character, broad strong-willed face, heavy jaw, impassive "
            "stoic expression, steel-gray piercing scanning eyes with heavy "
            "eyelids, short dark buzzcut hair with significant gray, clean-shaven, "
            "large broad-shouldered build with military bearing, mid to late 40s, "
            "deep vertical furrow between eyebrows"
        ),
        colors={"primary": "#607D8B", "secondary": "#0D47A1", "accent": "#B71C1C"},
        ref_front="igor-derzhavin-ref-front.png",
        ref_profile="igor-derzhavin-ref-profile.png",
        ref_fullbody="igor-derzhavin-ref-fullbody.png",
    ),
    "артём рыночный": Character(
        name_ru="Артём Рыночный",
        name_en="Artem Rynochny",
        role="Либерал-экономист",
        prompt_anchor=(
            "Male character, lean sharp face, raised eyebrow showing skepticism "
            "and irony, dark-brown quick appraising eyes, neatly styled dark hair "
            "slicked to the side in business cut, fit athletic build, mid-30s, "
            "one sleeve of jacket or shirt always rolled up"
        ),
        colors={"primary": "#1A237E", "secondary": "#FAFAFA", "accent": "#FFC107"},
        ref_front="artem-rynochny-ref-front.png",
        ref_profile="artem-rynochny-ref-profile.png",
        ref_fullbody="artem-rynochny-ref-fullbody.png",
    ),
}


def find_character(query: str) -> Optional[Character]:
    """Find character by name (case-insensitive, partial match)."""
    query_lower = query.lower().strip()
    if query_lower in CHARACTERS:
        return CHARACTERS[query_lower]
    for key, char in CHARACTERS.items():
        if query_lower in key or query_lower in char.name_en.lower():
            return char
    return None


def list_characters() -> list[Character]:
    """Return all available characters."""
    return list(CHARACTERS.values())


def build_prompt(
    character: Character,
    scene: str,
    clothing: Optional[str] = None,
    tech_params: str = "square crop, Telegram avatar format",
) -> str:
    """Build a full prompt from character data and scene description.

    Formula: [Style] + [Prompt Anchor] + [Clothing/Scene] + [Tech params]
    """
    parts = [
        STYLE_BLOCK + ".",
        "",
        character.prompt_anchor + ".",
        "",
    ]

    scene_parts = []
    if clothing:
        scene_parts.append(clothing + ".")
    scene_parts.append(scene + ".")

    parts.append(" ".join(scene_parts))
    parts.append("")
    parts.append(tech_params + ".")

    return "\n".join(parts)


def get_reference_image_path(
    character: Character,
    view: str = "front",
    workspace_root: Optional[Path] = None,
) -> Optional[Path]:
    """Get absolute path to a character's reference image."""
    ref_map = {
        "front": character.ref_front,
        "profile": character.ref_profile,
        "fullbody": character.ref_fullbody,
    }
    filename = ref_map.get(view)
    if not filename:
        return None

    base = workspace_root or Path(".")
    return base / REFERENCE_IMAGES_DIR / filename
