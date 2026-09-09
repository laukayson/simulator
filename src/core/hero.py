from dataclasses import dataclass

# Handles scaling stats based on level
@dataclass
class StatGrowth:
    base: float
    growth_per_level: float

    def value_at_level(self, level: int) -> float:
        return self.base + self.growth_per_level * (level - 1)

# Template holding base values for hero stats
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
    phy_pen: float = 0.0
    mag_pen: float = 0.0
    lifesteal: float = 0.0
    spell_vamp: float = 0.0
    cdr: float = 0.0
    hybrid_lifesteal: float = 0.0
    hybrid_def: float = 0.0
    hybrid_regen: float = 0.0
    adaptive_atk: float = 0.0
    adaptive_pen: float = 0.0

# Tracks HP and mana state while dynamically computing overall stats
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

    @property
    def phy_def(self) -> float:
        bonus = sum(getattr(item, "phy_def_bonus", 0.0) for item in self.build)
        return self._base_stats.phy_def + bonus

    @property
    def mag_def(self) -> float:
        bonus = sum(getattr(item, "mag_def_bonus", 0.0) for item in self.build)
        return self._base_stats.mag_def + bonus

    @property
    def atk_spd(self) -> float:
        bonus = sum(getattr(item, "atk_spd_bonus", 0.0) for item in self.build)
        return self._base_stats.atk_spd + bonus

    @property
    def atk_spd_ratio(self) -> float:
        return self._base_stats.atk_spd_ratio

    @property
    def crit_dmg(self) -> float:
        bonus = sum(getattr(item, "crit_dmg_bonus", 0.0) for item in self.build)
        return self._base_stats.crit_dmg + bonus

    @property
    def move_spd(self) -> float:
        bonus = sum(getattr(item, "move_spd_bonus", 0.0) for item in self.build)
        return self._base_stats.move_spd + bonus

    @property
    def ba_range(self) -> float:
        bonus = sum(getattr(item, "ba_range_bonus", 0.0) for item in self.build)
        return self._base_stats.ba_range + bonus

    @property
    def crit_chance(self) -> float:
        bonus = sum(getattr(item, "crit_chance_bonus", 0.0) for item in self.build)
        return self._base_stats.crit_chance + bonus

    @property
    def phy_pen(self) -> float:
        bonus = sum(getattr(item, "phy_pen_bonus", 0.0) for item in self.build)
        return self._base_stats.phy_pen + bonus

    @property
    def mag_pen(self) -> float:
        bonus = sum(getattr(item, "mag_pen_bonus", 0.0) for item in self.build)
        return self._base_stats.mag_pen + bonus

    @property
    def lifesteal(self) -> float:
        bonus = sum(getattr(item, "lifesteal_bonus", 0.0) for item in self.build)
        return self._base_stats.lifesteal + bonus

    @property
    def spell_vamp(self) -> float:
        bonus = sum(getattr(item, "spell_vamp_bonus", 0.0) for item in self.build)
        return self._base_stats.spell_vamp + bonus

    @property
    def cdr(self) -> float:
        bonus = sum(getattr(item, "cdr_bonus", 0.0) for item in self.build)
        return min(0.40, self._base_stats.cdr + bonus)