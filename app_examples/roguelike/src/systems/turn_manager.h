#pragma once

#include "../entities/champion.h"
#include "../entities/enemy.h"
#include "../entities/item.h"
#include "../entities/portal.h"
#include "../map/dungeon.h"
#include <vector>

namespace rl {

class TurnManager {
public:
    void process_player_turn(Direction dir, Champion& champion, std::vector<Enemy>& enemies,
                             Dungeon& dungeon, std::vector<std::string>& messages);
    void process_enemy_turn(std::vector<Enemy>& enemies, Champion& champion,
                            Dungeon& dungeon, std::vector<std::string>& messages);

private:
    bool try_move_champion(Champion& champion, Direction dir, const Dungeon& dungeon,
                           const std::vector<Enemy>& enemies,
                           std::vector<Enemy>& enemies_ref,
                           std::vector<std::string>& messages);
};

}
