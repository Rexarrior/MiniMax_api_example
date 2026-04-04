#include "generator.h"
#include "../core/random.h"

namespace rl {

Dungeon DungeonGenerator::generate(Biome biome) {
    Dungeon dungeon;

    switch (biome) {
        case Biome::Cave:
            dungeon.generate_cellular(biome);
            break;
        case Biome::Dungeon:
        case Biome::Forest:
        default:
            dungeon.generate_bsp(biome);
            break;
    }

    return dungeon;
}

}
