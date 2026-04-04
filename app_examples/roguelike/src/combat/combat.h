#pragma once

#include "../entities/champion.h"
#include "../entities/enemy.h"
#include <string>

namespace rl {

struct CombatResult {
    int damage_dealt = 0;
    bool critical = false;
    bool killed = false;
    std::string message;
};

CombatResult champion_attacks(const Champion& champion, Enemy& enemy);
CombatResult enemy_attacks(const Enemy& enemy, Champion& champion);

}
