#pragma once

#include "dungeon.h"

namespace rl {

class DungeonGenerator {
public:
    static Dungeon generate(Biome biome);
};

}
