#include "turn_manager.h"
#include "../ai/ai_system.h"
#include "../combat/combat.h"
#include "../core/config.h"
#include <algorithm>

namespace rl {

void TurnManager::process_player_turn(Direction dir, Champion& champion,
                                       std::vector<Enemy>& enemies,
                                       Dungeon& dungeon,
                                       MessageLog& log) {
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
            log.add(result.message);
            if (result.killed) {
                champion.gain_xp(enemy.xp_value());
                log.add("Gained " + std::to_string(enemy.xp_value()) + " XP");
            }
            // Both attack - set attack animation for both
            champion.set_attack_timer(ATTACK_ANIMATION_DURATION);
            enemy.set_attack_timer(ATTACK_ANIMATION_DURATION);
            return;
        }
    }

    if (dungeon.is_walkable(target.x, target.y)) {
        champion.set_moving(true);
        champion.move(dir);
        champion.set_moving(false);
    }
}

void TurnManager::process_enemy_turn(std::vector<Enemy>& enemies, Champion& champion,
                                      Dungeon& dungeon,
                                      MessageLog& log) {
    AISystem ai;
    ai.update(enemies, champion, dungeon);

    for (auto& enemy : enemies) {
        if (!enemy.alive()) continue;
        auto epos = enemy.pos();
        auto cpos = champion.pos();

        if (std::abs(epos.x - cpos.x) + std::abs(epos.y - cpos.y) <= 1) {
            auto result = enemy_attacks(enemy, champion);
            log.add(result.message);
            // Both attack - set attack animation for both
            enemy.set_attack_timer(ATTACK_ANIMATION_DURATION);
            champion.set_attack_timer(ATTACK_ANIMATION_DURATION);
            if (result.killed) return;
        }
    }
}

}
