from dataclasses import dataclass

@dataclass
class StatGrowth:
    base: float
    growth_per_level: float

    def value_at_level(self, level: int) -> float:
        return self.base + self.growth_per_level * (level - 1)

@dataclass
class BaseStats:
    hp: float
    hp_regen: float
    mana: float
    mana_regen: float
    phy_atk: float
    mag_pow: float
    phy_def: float
    mag_def: float
    atk_spd: float
    atk_spd_ratio: float
    crit_dmg: float
    move_spd: float
    ba_range: float
    crit_chance: float = 0.0


class Hero:
    def  __init__(
        self,
        name: str,
        base_stats: BaseStats,
        level: int = 1,
    ):
        self.name = name
        self.level = level
        self._base_stats = base_stats

        self._curr_hp: float = base_stats.hp
        self._curr_mana: float = base_stats.mana

        self.build: list = []
        self.skills: list = []

    @property
    def max_hp(self) -> float:
        hp_bonus = sum(getattr(item, "hp_bonus", 0.0) for item in self.build)
        return self._base_stats.hp + hp_bonus

    @property
    def hp(self) -> float:
        return self._curr_hp

    @hp.setter
    def hp(self, value: float) -> None:
        self._curr_hp = max(0.0, min(value, self.max_hp))

    @property
    def max_mana(self) -> float:
        mana_bonus = sum(getattr(item, "mana_bonus", 0.0) for item in self.build)
        return self._base_stats.mana + mana_bonus

    @property
    def mana(self) -> float:
        return self._curr_mana

    @mana.setter
    def mana(self, value: float) -> None:
        self._curr_mana = max(0.0, min(value, self.max_mana))

    @property
    def phy_atk(self) -> float:
        bonus = sum(getattr(item, "phy_atk_bonus", 0.0) for item in self.build)
        return self._base_stats.phy_atk + bonus

    @property
    def mag_pow(self) -> float:
        bonus = sum(getattr(item, "mag_pow_bonus", 0.0) for item in self.build)
        return self._base_stats.mag_pow + bonus