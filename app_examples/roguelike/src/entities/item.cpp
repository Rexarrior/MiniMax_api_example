#include "item.h"

namespace rl {

Item Item::make_potion(Position pos) {
    return {pos, ItemType::HealthPotion, "Health Potion", 15, false};
}

Item Item::make_gold(Position pos, int amount) {
    return {pos, ItemType::Gold, "Gold", amount, false};
}

}
