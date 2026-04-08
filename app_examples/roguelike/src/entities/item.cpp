#include "item.h"

namespace rl {

Item Item::make_potion(Position pos) {
    return {pos, ItemType::HealthPotion, "Health Potion", 15, false, "", ActionState::Idle};
}

Item Item::make_gold(Position pos, int amount) {
    return {pos, ItemType::Gold, "Gold", amount, false, "", ActionState::Idle};
}

Item Item::make_prop_healing_herbs(Position pos) {
    return {pos, ItemType::PropHealingHerbs, "Healing Herbs", 0, false, "healing_herbs_and_potions", ActionState::Idle};
}

Item Item::make_prop_mushrooms(Position pos) {
    return {pos, ItemType::PropMushrooms, "Mushrooms", 0, false, "mushrooms_and_fungi", ActionState::Idle};
}

}
