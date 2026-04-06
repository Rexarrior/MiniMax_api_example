#pragma once

#include "../entities/enemy.h"
#include "../entities/champion.h"
#include "../map/dungeon.h"
#include <vector>

namespace rl {

class AISystem {
public:
    void update(std::vector<Enemy>& enemies, const Champion& champion, const Dungeon& dungeon);
    void move_enemy(Enemy& enemy, const Champion& champion, const Dungeon& dungeon);
};

}
