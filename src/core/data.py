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