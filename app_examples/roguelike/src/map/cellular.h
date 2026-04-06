#pragma once

#include "dungeon.h"

namespace rl {

class CellularGenerator {
public:
    static Dungeon generate(int wall_fill_percent = 45, int smoothing_iterations = 5);
};

}
