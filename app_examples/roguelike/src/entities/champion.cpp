#include "champion.h"
#include <algorithm>

namespace rl {

Champion::Champion(Position pos)
    : Entity(pos, EntityType::Champion, "champion") {
    stats_ = {30, 30, 5, 3, 1};
}

void Champion::move(Direction dir) {
    switch (dir) {
        case Direction::Up:    --pos_.y; break;
        case Direction::Down:  ++pos_.y; break;
        case Direction::Left:  --pos_.x; break;
        case Direction::Right: ++pos_.x; break;
        default: break;
    }
}

void Champion::gain_xp(int amount) {
    xp_ += amount;
    int needed = level_ * 15;
    while (xp_ >= needed) {
        xp_ -= needed;
        ++level_;
        stats_.max_hp += 5;
        stats_.hp = stats_.max_hp;
        stats_.attack += 1;
        stats_.defense += 1;
        needed = level_ * 15;
    }
}

void Champion::use_potion() {
    if (potions_ > 0) {
        --potions_;
        stats_.hp = std::min(stats_.hp + 15, stats_.max_hp);
    }
}

}
