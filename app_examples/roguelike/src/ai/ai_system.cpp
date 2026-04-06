#include "ai_system.h"
#include "behaviors.h"
#include "../core/random.h"

namespace rl {

void AISystem::update(std::vector<Enemy>& enemies, const Champion& champion, const Dungeon& dungeon) {
    for (auto& enemy : enemies) {
        if (!enemy.alive()) continue;
        move_enemy(enemy, champion, dungeon);
    }
}

void AISystem::move_enemy(Enemy& enemy, const Champion& champion, const Dungeon& dungeon) {
    auto pos = enemy.pos();
    auto cpos = champion.pos();

    int dx = cpos.x - pos.x;
    int dy = cpos.y - pos.y;
    int dist = std::abs(dx) + std::abs(dy);

    if (dist <= 1) return;

    if (dist > 12) {
        if (RNG::instance().chance(30)) return;
    }

    int move_x = 0, move_y = 0;

    if (std::abs(dx) >= std::abs(dy)) {
        move_x = (dx > 0) ? 1 : -1;
        if (!dungeon.is_walkable(pos.x + move_x, pos.y)) {
            move_x = 0;
            move_y = (dy > 0) ? 1 : -1;
        }
    } else {
        move_y = (dy > 0) ? 1 : -1;
        if (!dungeon.is_walkable(pos.x, pos.y + move_y)) {
            move_y = 0;
            move_x = (dx > 0) ? 1 : -1;
        }
    }

    if (dungeon.is_walkable(pos.x + move_x, pos.y + move_y)) {
        enemy.set_pos({pos.x + move_x, pos.y + move_y});
    }
}

}
