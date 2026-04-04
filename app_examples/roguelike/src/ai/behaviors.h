#pragma once

#include "../entities/enemy.h"
#include "../entities/champion.h"
#include "../map/dungeon.h"

namespace rl {

struct BehaviorResult {
    int dx = 0;
    int dy = 0;
    bool wants_attack = false;
};

BehaviorResult chase_behavior(const Enemy& enemy, const Champion& champion, const Dungeon& dungeon);
BehaviorResult patrol_behavior(const Enemy& enemy, const Dungeon& dungeon);
BehaviorResult flee_behavior(const Enemy& enemy, const Champion& champion, const Dungeon& dungeon);

}
