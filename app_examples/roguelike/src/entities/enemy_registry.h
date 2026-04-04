#pragma once

#include "enemy.h"
#include "../core/random.h"
#include <vector>

namespace rl {

class EnemyRegistry {
public:
    static std::vector<EnemyType> all_types();
    static EnemyType random_for_floor(int floor);
    static EnemyType random_weak();
    static EnemyType random_medium();
    static EnemyType random_strong();
};

}
