#pragma once

#include "../core/types.h"
#include "entity.h"
#include <string>

namespace rl {

enum class ItemType {
    HealthPotion,
    StrengthBoost,
    DefenseBoost,
    Gold,
    PropHealingHerbs,
    PropMushrooms,
};

struct Item {
    Position pos;
    ItemType type;
    std::string name;
    int value;
    bool picked_up = false;

    // For props with animated sprites
    std::string sprite_name;
    ActionState action_state = ActionState::Idle;

    static Item make_potion(Position pos);
    static Item make_gold(Position pos, int amount);
    static Item make_prop_healing_herbs(Position pos);
    static Item make_prop_mushrooms(Position pos);

    std::string full_sprite_name() const {
        if (sprite_name.empty()) return "";
        return sprite_name + Entity::action_to_string(action_state);
    }
};

}
