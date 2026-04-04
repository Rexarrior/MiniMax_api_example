#pragma once

#include "../core/types.h"
#include <string>

namespace rl {

enum class ItemType {
    HealthPotion,
    StrengthBoost,
    DefenseBoost,
    Gold,
};

struct Item {
    Position pos;
    ItemType type;
    std::string name;
    int value;
    bool picked_up = false;

    static Item make_potion(Position pos);
    static Item make_gold(Position pos, int amount);
};

}
