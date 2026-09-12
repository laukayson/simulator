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
    lifesteal: float = 0.0
    spell_vamp: float = 0.0
    cdr: float = 0.0
    hybrid_lifesteal: float = 0.0
    hybrid_def: float = 0.0
    hybrid_regen: float = 0.0
    adaptive_atk: float = 0.0
    adaptive_pen: float = 0.0

# Master lookup table for Level 60 emblem attributes
base_emblems = {
    "Basic Common": {
        "hybrid_regen_flat_bonus": 12.0,
        "hp_flat_bonus": 275.0,
        "adaptive_atk_flat_bonus": 22.0,
    },
    "Tank": {
        "hp_flat_bonus": 500.0,
        "hybrid_def_flat_bonus": 10.0,
        "hp_regen_flat_bonus": 4.0,
    },
    "Assassin": {
        "adaptive_pen_flat_bonus": 14.0,
        "adaptive_atk_flat_bonus": 10.0,
        "move_spd_pct_bonus": 0.03,
    },
    "Mage": {
        "mag_pow_flat_bonus": 30.0,
        "cdr_pct_bonus": 0.05,
        "mag_pen_flat_bonus": 0.08,
    },
    "Fighter": {
        "hybrid_lifesteal_pct_bonus": 0.10,
        "adaptive_atk_flat_bonus": 16.0,
        "hybrid_def_flat_bonus": 8.0,
    },
    "Support": {
        "healing_effect_pct_bonus": 0.12,
        "cdr_pct_bonus": 0.10,
        "move_spd_pct_bonus": 0.06,
    },
    "Marksman": {
        "atk_spd_pct_bonus": 0.15,
        "adaptive_atk_flat_bonus": 16.0,
        "adaptive_pen_pct_bonus": 0.10,
    }
}

# Master lookup table for Tier 1 talents
t1_talents = {
    "Thrill": {"adaptive_atk_flat_bonus": 16.0},
    "Swift": {"atk_spd_pct_bonus": 0.10},
    "Vitality": {"hp_flat_bonus": 225.0},
    "Rupture": {"adaptive_pen_flat_bonus": 5.0},
    "Inspire": {"cdr_pct_bonus": 0.05, "mana_regen_flat_bonus": 2.0},
    "Firmness": {"phy_def_flat_bonus": 8.0, "mag_def_flat_bonus": 8.0},
    "Agility": {"move_spd_pct_bonus": 0.04},
    "Fatal": {"crit_chance_pct_bonus": 0.05, "crit_dmg_pct_bonus": 0.05},
}

# Tracks HP and mana state while dynamically computing overall stats
class Hero:
    def  __init__(
        self,
        name: str,
        base_stats: BaseStats,
        level: int = 1,
        emblem: any = None,
        primary_dmg: str = "phy",
    ):
        self.name = name
        self.level = level
        self._base_stats = base_stats
        self.emblem = emblem
        self.primary_dmg = primary_dmg

        self._curr_hp: float = base_stats.hp
        self._curr_mana: float = base_stats.mana

        self.build: list = []
        self.skills: list = []

    def _get_stat_sources(self) -> list:
        sources = []
        if self.emblem:
            sources.append(self.emblem)
        sources.extend(self.build)
        return sources

    def _sum_stat(self, attr_name: str) -> float:
        return sum(getattr(source, attr_name, 0.0) for source in self._get_stat_sources())

    @property
    def max_hp(self) -> float:
        flat = self._sum_stat("hp_flat_bonus")
        pct = self._sum_stat("hp_pct_bonus")
        return (self._base_stats.hp + flat) * (1 + pct)

    @property
    def hp(self) -> float:
        return self._curr_hp

    @hp.setter
    def hp(self, value: float) -> None:
        self._curr_hp = max(0.0, min(value, self.max_hp))

    @property
    def max_mana(self) -> float:
        flat = self._sum_stat("mana_flat_bonus")
        pct = self._sum_stat("mana_pct_bonus")
        return (self._base_stats.mana + flat) * (1 + pct)

    @property
    def mana(self) -> float:
        return self._curr_mana

    @mana.setter
    def mana(self, value: float) -> None:
        self._curr_mana = max(0.0, min(value, self.max_mana))

    @property
    def _get_extra_phy_atk(self) -> float:
        flat = self._sum_stat("phy_atk_flat_bonus")
        pct = self._sum_stat("phy_atk_pct_bonus")
        return (self._base_stats.phy_atk + flat) * (1 + pct) - self._base_stats.phy_atk

    @property
    def _get_extra_mag_pow(self) -> float:
        flat = self._sum_stat("mag_pow_flat_bonus")
        pct = self._sum_stat("mag_pow_pct_bonus")
        return (self._base_stats.mag_pow + flat) * (1 + pct) - self._base_stats.mag_pow

    @property
    def adaptive_type(self) -> str:
        if self._get_extra_phy_atk > self._get_extra_mag_pow:
            return "phy"
        if self._get_extra_mag_pow > self._get_extra_phy_atk:
            return "mag"
        return self.primary_dmg

    @property
    def adaptive_atk(self) -> float:
        return self._sum_stat("adaptive_atk_flat_bonus")

    @property
    def phy_atk(self) -> float:
        flat = self._sum_stat("phy_atk_flat_bonus")
        pct = self._sum_stat("phy_atk_pct_bonus")
        if self.adaptive_type == "phy":
            pct += self._sum_stat("adaptive_atk_pct_bonus")
            flat += self.adaptive_atk
        return (self._base_stats.phy_atk + flat) * (1 + pct)

    @property
    def mag_pow(self) -> float:
        flat = self._sum_stat("mag_pow_flat_bonus")
        pct = self._sum_stat("mag_pow_pct_bonus")
        if self.adaptive_type == "mag":
            pct += self._sum_stat("adaptive_atk_pct_bonus")
            flat += self.adaptive_atk
        return (self._base_stats.mag_pow + flat) * (1 + pct)

    @property
    def phy_def(self) -> float:
        flat = self._sum_stat("phy_def_flat_bonus")
        pct = self._sum_stat("phy_def_pct_bonus")
        return (self._base_stats.phy_def + flat) * (1 + pct)

    @property
    def mag_def(self) -> float:
        flat = self._sum_stat("mag_def_flat_bonus")
        pct = self._sum_stat("mag_def_pct_bonus")
        return (self._base_stats.mag_def + flat) * (1 + pct)

    @property
    def atk_spd(self) -> float:
        flat = self._sum_stat("atk_spd_flat_bonus")
        pct = self._sum_stat("atk_spd_pct_bonus")
        return (self._base_stats.atk_spd + flat) * (1 + pct)

    @property
    def atk_spd_ratio(self) -> float:
        return self._base_stats.atk_spd_ratio

    @property
    def crit_dmg(self) -> float:
        flat = self._sum_stat("crit_dmg_flat_bonus")
        pct = self._sum_stat("crit_dmg_pct_bonus")
        return (self._base_stats.crit_dmg + flat) * (1 + pct)

    @property
    def move_spd(self) -> float:
        flat = self._sum_stat("move_spd_flat_bonus")
        pct = self._sum_stat("move_spd_pct_bonus")
        return (self._base_stats.move_spd + flat) * (1 + pct)

    @property
    def ba_range(self) -> float:
        flat = self._sum_stat("ba_range_flat_bonus")
        pct = self._sum_stat("ba_range_pct_bonus")
        return (self._base_stats.ba_range + flat) * (1 + pct)

    @property
    def crit_chance(self) -> float:
        return self._base_stats.crit_chance + self._sum_stat("crit_chance_pct_bonus")
    
    @property
    def adaptive_pen(self) -> float:
        return self._sum_stat("adaptive_pen_flat_bonus")

    @property
    def phy_pen(self) -> float:
        if self.adaptive_type == "phy":
            return self._sum_stat("phy_pen_flat_bonus") + self._sum_stat("adaptive_pen_flat_bonus")
        return self._sum_stat("phy_pen_flat_bonus")

    @property
    def mag_pen(self) -> float:
        if self.adaptive_type == "mag":
            return self._sum_stat("mag_pen_flat_bonus") + self._sum_stat("adaptive_pen_flat_bonus")
        return self._sum_stat("mag_pen_flat_bonus")

    @property
    def lifesteal(self) -> float:
        return self._base_stats.lifesteal + self._sum_stat("lifesteal_pct_bonus")
    
    @property
    def spell_vamp(self) -> float:
        return self._base_stats.spell_vamp + self._sum_stat("spell_vamp_pct_bonus")

    @property
    def cdr(self) -> float:
        return min(0.40, self._base_stats.cdr + self._sum_stat("cdr_pct_bonus"))