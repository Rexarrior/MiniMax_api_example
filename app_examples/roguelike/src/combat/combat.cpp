#include "combat.h"
#include "../core/random.h"
#include <algorithm>

namespace rl {

CombatResult champion_attacks(const Champion& champion, Enemy& enemy) {
    CombatResult result;
    auto& rng = RNG::instance();

    int variance = rng.range(-2, 2);
    result.damage_dealt = std::max(1, champion.stats().attack - enemy.stats().defense + variance);

    result.critical = rng.chance(10);
    if (result.critical) {
        result.damage_dealt *= 2;
    }

    auto& e_stats = const_cast<Stats&>(enemy.stats());
    e_stats.hp -= result.damage_dealt;

    std::string name = Enemy::sprite_name_for(enemy.enemy_type());
    result.message = "You hit the " + name + " for " + std::to_string(result.damage_dealt) + " damage";
    if (result.critical) result.message += " (CRITICAL!)";

    if (e_stats.hp <= 0) {
        result.killed = true;
        enemy.kill();
        result.message += " — " + name + " is defeated!";
    }

    return result;
}

CombatResult enemy_attacks(const Enemy& enemy, Champion& champion) {
    CombatResult result;
    auto& rng = RNG::instance();

    int variance = rng.range(-1, 2);
    result.damage_dealt = std::max(1, enemy.stats().attack - champion.stats().defense + variance);

    result.critical = rng.chance(5);
    if (result.critical) {
        result.damage_dealt *= 2;
    }

    auto& c_stats = const_cast<Stats&>(champion.stats());
    c_stats.hp -= result.damage_dealt;

    std::string name = Enemy::sprite_name_for(enemy.enemy_type());
    result.message = "The " + name + " hits you for " + std::to_string(result.damage_dealt) + " damage";
    if (result.critical) result.message += " (CRITICAL!)";

    if (c_stats.hp <= 0) {
        result.killed = true;
        result.message += " — You have been slain!";
    }

    return result;
}

}
