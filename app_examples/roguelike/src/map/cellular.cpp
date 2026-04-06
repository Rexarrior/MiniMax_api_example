#include "cellular.h"
#include "../core/random.h"

namespace rl {

Dungeon CellularGenerator::generate(int wall_fill_percent, int smoothing_iterations) {
    Dungeon dungeon;
    auto& rng = RNG::instance();

    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            dungeon.set_tile(x, y, rng.chance(wall_fill_percent) ? TileType::Wall : TileType::Floor);

    dungeon.smooth_cellular(smoothing_iterations);
    return dungeon;
}

}
