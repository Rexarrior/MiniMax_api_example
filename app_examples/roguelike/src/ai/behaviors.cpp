#include "behaviors.h"
#include <cmath>

namespace rl {

BehaviorResult chase_behavior(const Enemy& enemy, const Champion& champion, const Dungeon& dungeon) {
    BehaviorResult result;
    auto pos = enemy.pos();
    auto cpos = champion.pos();

    int dx = cpos.x - pos.x;
    int dy = cpos.y - pos.y;

    if (std::abs(dx) + std::abs(dy) <= 1) {
        result.wants_attack = true;
        return result;
    }

    if (std::abs(dx) >= std::abs(dy)) {
        result.dx = (dx > 0) ? 1 : -1;
    } else {
        result.dy = (dy > 0) ? 1 : -1;
    }

    return result;
}

BehaviorResult patrol_behavior(const Enemy& enemy, const Dungeon& dungeon) {
    BehaviorResult result;
    static int patrol_dir = 0;
    auto pos = enemy.pos();

    const int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int i = 0; i < 4; ++i) {
        int d = (patrol_dir + i) % 4;
        if (dungeon.is_walkable(pos.x + dirs[d][0], pos.y + dirs[d][1])) {
            result.dx = dirs[d][0];
            result.dy = dirs[d][1];
            patrol_dir = d;
            break;
        }
    }

    return result;
}

BehaviorResult flee_behavior(const Enemy& enemy, const Champion& champion, const Dungeon& dungeon) {
    BehaviorResult result;
    auto pos = enemy.pos();
    auto cpos = champion.pos();

    int dx = pos.x - cpos.x;
    int dy = pos.y - cpos.y;

    if (dx != 0) result.dx = (dx > 0) ? 1 : -1;
    else if (dy != 0) result.dy = (dy > 0) ? 1 : -1;

    return result;
}

}
