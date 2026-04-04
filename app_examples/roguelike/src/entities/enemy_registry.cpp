#include "enemy_registry.h"

namespace rl {

std::vector<EnemyType> EnemyRegistry::all_types() {
    return {
        EnemyType::Skeleton, EnemyType::Goblin, EnemyType::Orc,
        EnemyType::GiantRat, EnemyType::GiantSpider, EnemyType::Slime,
        EnemyType::FireDemon, EnemyType::Ghost, EnemyType::Werewolf,
        EnemyType::DarkMage
    };
}

EnemyType EnemyRegistry::random_weak() {
    static const std::vector<EnemyType> weak = {
        EnemyType::Slime, EnemyType::GiantRat, EnemyType::Goblin, EnemyType::GiantSpider
    };
    return RNG::instance().pick(weak);
}

EnemyType EnemyRegistry::random_medium() {
    static const std::vector<EnemyType> medium = {
        EnemyType::Skeleton, EnemyType::Ghost, EnemyType::DarkMage, EnemyType::Werewolf
    };
    return RNG::instance().pick(medium);
}

EnemyType EnemyRegistry::random_strong() {
    static const std::vector<EnemyType> strong = {
        EnemyType::Orc, EnemyType::FireDemon
    };
    return RNG::instance().pick(strong);
}

EnemyType EnemyRegistry::random_for_floor(int floor) {
    auto& rng = RNG::instance();
    if (floor <= 2) return random_weak();
    if (floor <= 4) return rng.chance(70) ? random_medium() : random_weak();
    if (floor <= 6) return rng.chance(60) ? random_strong() : random_medium();
    return rng.chance(50) ? random_strong() : random_medium();
}

}
