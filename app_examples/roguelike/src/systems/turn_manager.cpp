#include "turn_manager.h"
#include "../ai/ai_system.h"
#include "../combat/combat.h"
#include <algorithm>

namespace rl {

void TurnManager::process_player_turn(Direction dir, Champion& champion,
                                       std::vector<Enemy>& enemies,
                                       Dungeon& dungeon,
                                       std::vector<std::string>& messages) {
    if (dir == Direction::None) return;

    auto pos = champion.pos();
    Position target = pos;
    switch (dir) {
        case Direction::Up:    --target.y; break;
        case Direction::Down:  ++target.y; break;
        case Direction::Left:  --target.x; break;
        case Direction::Right: ++target.x; break;
        default: break;
    }

    for (auto& enemy : enemies) {
        if (enemy.alive() && enemy.pos() == target) {
            auto result = champion_attacks(champion, enemy);
            messages.push_back(result.message);
            if (result.killed) {
                champion.gain_xp(enemy.xp_value());
                messages.push_back("Gained " + std::to_string(enemy.xp_value()) + " XP");
            }
            return;
        }
    }

    if (dungeon.is_walkable(target.x, target.y)) {
        champion.move(dir);
    }
}

void TurnManager::process_enemy_turn(std::vector<Enemy>& enemies, Champion& champion,
                                      Dungeon& dungeon,
                                      std::vector<std::string>& messages) {
    AISystem ai;
    ai.update(enemies, champion, dungeon);

    for (auto& enemy : enemies) {
        if (!enemy.alive()) continue;
        auto epos = enemy.pos();
        auto cpos = champion.pos();

        if (std::abs(epos.x - cpos.x) + std::abs(epos.y - cpos.y) <= 1) {
            auto result = enemy_attacks(enemy, champion);
            messages.push_back(result.message);
            if (result.killed) return;
        }
    }
}

}
