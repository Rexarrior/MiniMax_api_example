#pragma once

#include "../entities/champion.h"
#include "../entities/enemy.h"
#include "../entities/item.h"
#include "../entities/portal.h"
#include "../map/dungeon.h"
#include "../ui/message_log.h"
#include <vector>

namespace rl {

class TurnManager {
public:
    void process_player_turn(Direction dir, Champion& champion, std::vector<Enemy>& enemies,
                             Dungeon& dungeon, MessageLog& log);
    void process_enemy_turn(std::vector<Enemy>& enemies, Champion& champion,
                            Dungeon& dungeon, MessageLog& log);

private:
};

}
