"""All items"""
# pylint: disable=missing-class-docstring
from enum import Enum
from IPython.display import display, Math


class ItemType(Enum):
    ATTACK = "Attack"  # Increases damage, or related
    HEAL = "Heal"
    DEFENSE = "Defense"  # Increases health, armor barrier or shield, reduces damage, or related
    SUPPORT = "Support"  # Other combat-related bonuses
    MISC = "Misc."    # Other miscellaneous bonuses


class Scaler():  # pylint: disable=missing-class-docstring
    def __init__(self, inc, base):
        self.base = base
        self.inc = inc
        self.func = lambda x: x
        self.description = "f(x) = x"
        self.latex = Math("f(x) = x")

    def effect_at(self, count):  # pylint: disable=missing-function-docstring
        return self.func(count) if count != 0 else 0

    def display(self):  # pylint: disable=missing-function-docstring
        display(self.latex)

    def __str__(self):
        return self.description


class Linear(Scaler):
    scale_type = "linear"

    def __init__(self, inc, base=0):
        super().__init__(inc, base)
        self.description = f"f(x) = {base} + {inc}x"
        self.latex      = f"$f(x) = {base} + {inc}x$"
        self.func = lambda count: base + inc*count


class Hyperbolic(Scaler):
    scale_type = "hyperbolic"

    def __init__(self, inc):
        super().__init__(inc, 0)
        self.description = f"f(x) = 1 - 1/(1 + {inc}x)"
        self.latex      = f"$f(x) = 1 - \\dfrac{{1}}{{1 + {inc}x}}$"
        self.func = lambda count: 1 - 1/(1 + inc*count)


class Exponential(Scaler):
    scale_type = "hyperbolic"

    def __init__(self, inc):
        super().__init__(inc, 0)
        self.description = f"f(x) = {inc}x"
        self.latex      = f"$f(x) = {inc}^{{x}}$"
        self.func = lambda count: inc**count


class Bandolier(Scaler):
    scale_type = "hyperbolic"

    def __init__(self):
        super().__init__(0, 0)
        self.description = "f(x) = 1 - 1/(1 + x)^0.33"
        self.latex      = "$f(x) = 1 - \\dfrac{{1}}{{(1 + x)^{{0.33}}}}$"
        self.func = lambda count: 1 - 1/pow(1 + count, 0.33)


class Item:  # pylint: disable=missing-class-docstring
    def __init__(self, name, desc, _types, effects):
        self.name = name
        self.description = desc
        self.types = _types
        self.effects = effects

# COMMON ITEMS


common_items = dict(

    ap_rounds=Item(
        r"Armor-Piercing Rounds",
        r"Deal an additional 20% damage (+20% per stack) to bosses",
        [ItemType.ATTACK],
        {
            "Damage to Bosses": Linear(0.2, 1)
        }
    ),

    backup_magazine=Item(
        r"Backup Magazine",
        r"Add +1 (+1 per stack) charge of your Secondary skill",
        [ItemType.SUPPORT],
        {
            "Bonus Secondary Skill Charges": Linear(1, 0)
        }
    ),

    bison_steak=Item(
        r"Bison Steak",
        r"Increases maximum health by 25 (+25 per stack)",
        [ItemType.DEFENSE],
        {
            "Max Health Increase": Linear(25, 0)
        }
    ),

    bundle_of_fireworks=Item(
        r"Bundle of Fireworks",
        r"Activating an interactable launches 8 (+4 per stack) fireworks that deal 300% base damage",
        [ItemType.MISC],
        {
            "Fireworks on Interacting": Linear(4, 4)
        }
    ),

    bustling_fungus=Item(
        r"Bustling Fungus",
        r"After standing still for 1 second, create a zone that heals for 4.5% (+2.25% per stack) of your health every second to all allies within 3m (+1.5m per stack)",
        [ItemType.HEAL],
        {

            "Heal Percent on Standing Still": Linear(0.0225, 0.0225),
            "Heal Range on Standing Still": Linear(1.5, 1.5)
        }
    ),

    cautious_slug=Item(
        r"Cautious Slug",
        r"Increases base health regeneration by +3 hp/s (+3 hp/s per stack) while outside of combat",
        [ItemType.HEAL],
        {
            "Heal Amount Outside Combat": Linear(3, 0)
        }
    ),

    crowbar=Item(
        r"Crowbar",
        r"Deal +75% (+75% per stack) damage to enemies above 90% health",
        [ItemType.ATTACK],
        {
            "Bonus Damage to Enemies at Full Health": Linear(0.75, 1)
        }
    ),

    delicate_watch=Item(
        r"Delicate Watch",
        r"Increase damage by 20% (+20% per stack). Taking damage to below 25% health breaks this item",
        [ItemType.ATTACK],
        {
            "Bonus Damage": Linear(0.2, 1)
        }
    ),

    energy_drink=Item(
        r"Energy Drink",
        r"Sprint speed is improved by 25% (+25% per stack)",
        [ItemType.SUPPORT],
        {
            "Bonus Sprint Speed": Linear(0.25, 1)
        }
    ),

    focus_crystal=Item(
        r"Focus Crystal",
        r"Increase damage to enemies within 13m by 20% (+20% per stack)",
        [ItemType.ATTACK],
        {
            "Bonus Damage to Nearby Enemies": Linear(0.20, 1)
        }
    ),

    gasoline=Item(
        r"Gasoline",
        r"Killing an enemy ignites all enemies within 12m (+4m per stack) for 150% base damage. Additionally, enemies burn for 150% (+75% per stack) base damage",
        [ItemType.ATTACK],
        {
            "Ignite Range on Kill": Linear(4, 8),
            "Burn Damage over Time": Linear(0.75, 0.75)
        }
    ),

    lens_makers_glasses=Item(
        r"Lens-Maker's Glasses",
        r"Your attacks have a 10% (+10% per stack) chance to 'Critically Strike', dealing double damage",
        [ItemType.ATTACK],
        {
            "Crit. Chance": Linear(0.10, 0)
        }
    ),

    medkit=Item(
        r"Medkit",
        r"2 seconds after getting hurt, heal for 20 plus an additional 5% (+5% per stack) of maximum health",
        [ItemType.HEAL],
        {
            "Heal After Taking Damage": Linear(0.05, 0)
        }
    ),

    mocha=Item(
        r"Mocha",
        r"Increases attack speed by 7.5% (+7.5 per stack) and movement speed by 7% (+7% per stack)",
        [ItemType.ATTACK, ItemType.SUPPORT],
        {
            "Bonus Attack Speed": Linear(0.075, 0),
            "Bonus Move Speed": Linear(0.07, 0)
        }
    ),

    monster_tooth=Item(
        r"Monster Tooth",
        r"Killing an enemy spawns a healing orb that heals for 8 plus an additional 2% (+2% per stack) of maximum health",
        [ItemType.HEAL],
        {  
            "Base Heal on Kill": Linear(0, 8),
            "Heal on Kill": Linear(0.02, 0)
        }
    ),

    oddly_shapped_opal=Item(
        r"Oddly-Shaped Opal",
        r"Increase armor by 100 (+100 per stack) while out of danger",
        [ItemType.DEFENSE],
        {
            "Armor While Out of Danger": Linear(100, 0)
        }
    ),

    pauls_goat_hoof=Item(
        r"Paul's Goat Hoof",
        r"Increases movement speed by 14% (+14% per stack)",
        [ItemType.SUPPORT],
        {
            "Bonus Move Speed": Linear(0.14, 1)
        }
    ),

    personal_shield_generator=Item(
        r"Personal Shield Generator",
        r"Gain a shield equal to 8% (+8% per stack) of your maximum health. Recharges outside of danger",
        [ItemType.DEFENSE],
        {
            "Bonus Shield": Linear(0.08, 1)
        }
    ),

    power_elixir=Item(
        r"Power Elixir",
        r"Taking damage to below 25% health consumes this item, healing you for 75% of maximum health",
        [ItemType.HEAL],
        {
            "Heals When Low Health": Linear(1, 0)
        }
    ),

    repulsion_armor_plate=Item(
        r"Repulsion Armor Plate",
        r"Reduce all incoming damage by 5 (+5 per stack). Cannot be reduced below 1",
        [ItemType.DEFENSE],
        {
            "Damage Reduction": Linear(5, 0)
        }
    ),


)

