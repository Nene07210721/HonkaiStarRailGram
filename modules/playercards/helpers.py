import os

import ujson as json

from modules.playercards.fight_prop import FightPropScore, EquipmentsStats, nameToFightProp
from modules.wiki.models.enums import RelicAffix

_project_path = os.path.dirname(__file__)
_fight_prop_rule_file = os.path.join(_project_path, "metadata", "FightPropRule.json")
with open(_fight_prop_rule_file, "r", encoding="utf-8") as f:
    fight_prop_rule_data: dict = json.load(f)


class ArtifactStatsTheory:
    def __init__(self, character_name: str):
        self.character_name = character_name
        fight_prop_rule_list = fight_prop_rule_data.get(self.character_name, [])
        self.main_prop = [nameToFightProp(fight_prop_rule) for fight_prop_rule in fight_prop_rule_list]
        if not self.main_prop:
            self.main_prop = [
                RelicAffix.CriticalChanceBase,
                RelicAffix.CriticalDamageBase,
                RelicAffix.AttackAddedRatio,
            ]

    def theory(self, sub_stats: EquipmentsStats) -> float:
        """圣遗物词条评分
        Args:
            sub_stats: 圣遗物对象
        Returns:
            返回得分
        """
        score: float = 0
        if sub_stats.prop_id in self.main_prop:
            base_value = 100.0 if sub_stats.prop_value < 1 else 1.0
            score = float(FightPropScore(sub_stats.prop_id) * sub_stats.prop_value * base_value)
        return round(score, 1)
