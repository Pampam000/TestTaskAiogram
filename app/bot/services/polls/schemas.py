from dataclasses import dataclass


@dataclass
class Poll:
    group_id: str
    question: str
    variants: list[str]
