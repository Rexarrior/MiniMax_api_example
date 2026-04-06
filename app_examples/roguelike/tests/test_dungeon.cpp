#include <gtest/gtest.h>
#include "map/dungeon.h"
#include "core/config.h"
#include "core/random.h"

using namespace rl;

class DungeonTest : public ::testing::Test {
protected:
    void SetUp() override {
        RNG::instance().seed(42);
    }
};

TEST_F(DungeonTest, DefaultIsAllWalls) {
    Dungeon d;
    for (int y = 0; y < MAP_HEIGHT; ++y) {
        for (int x = 0; x < MAP_WIDTH; ++x) {
            EXPECT_EQ(d.tile_at(x, y), TileType::Wall)
                << "Expected wall at (" << x << "," << y << ")";
        }
    }
}

TEST_F(DungeonTest, SetAndGetTile) {
    Dungeon d;
    d.set_tile(5, 5, TileType::Floor);
    EXPECT_EQ(d.tile_at(5, 5), TileType::Floor);
}

TEST_F(DungeonTest, SetTileOutOfBounds) {
    Dungeon d;
    d.set_tile(-1, 0, TileType::Floor);
    d.set_tile(MAP_WIDTH, 0, TileType::Floor);
    d.set_tile(0, -1, TileType::Floor);
    d.set_tile(0, MAP_HEIGHT, TileType::Floor);
    EXPECT_EQ(d.tile_at(-1, 0), TileType::Wall);
    EXPECT_EQ(d.tile_at(MAP_WIDTH, 0), TileType::Wall);
    EXPECT_EQ(d.tile_at(0, -1), TileType::Wall);
    EXPECT_EQ(d.tile_at(0, MAP_HEIGHT), TileType::Wall);
}

TEST_F(DungeonTest, IsWalkableFloor) {
    Dungeon d;
    d.set_tile(10, 10, TileType::Floor);
    EXPECT_TRUE(d.is_walkable(10, 10));
}

TEST_F(DungeonTest, IsWalkableWall) {
    Dungeon d;
    EXPECT_FALSE(d.is_walkable(0, 0));
}

TEST_F(DungeonTest, IsWalkableOutOfBounds) {
    Dungeon d;
    EXPECT_FALSE(d.is_walkable(-1, 0));
    EXPECT_FALSE(d.is_walkable(MAP_WIDTH, 0));
    EXPECT_FALSE(d.is_walkable(0, -1));
    EXPECT_FALSE(d.is_walkable(0, MAP_HEIGHT));
}

TEST_F(DungeonTest, IsInBounds) {
    Dungeon d;
    EXPECT_TRUE(d.is_in_bounds(0, 0));
    EXPECT_TRUE(d.is_in_bounds(MAP_WIDTH - 1, MAP_HEIGHT - 1));
    EXPECT_TRUE(d.is_in_bounds(1, 1));
    EXPECT_FALSE(d.is_in_bounds(-1, 0));
    EXPECT_FALSE(d.is_in_bounds(MAP_WIDTH, 0));
    EXPECT_FALSE(d.is_in_bounds(0, -1));
    EXPECT_FALSE(d.is_in_bounds(0, MAP_HEIGHT));
}

TEST_F(DungeonTest, BSPGeneratesRooms) {
    Dungeon d;
    d.generate_bsp(Biome::Dungeon);
    EXPECT_GT(d.rooms().size(), 0u);
}

TEST_F(DungeonTest, BSPRoomsAreFloors) {
    Dungeon d;
    d.generate_bsp(Biome::Dungeon);
    for (const auto& room : d.rooms()) {
        EXPECT_EQ(d.tile_at(room.center_x(), room.center_y()), TileType::Floor);
    }
}

TEST_F(DungeonTest, BSPBiome) {
    Dungeon d;
    d.generate_bsp(Biome::Forest);
    EXPECT_EQ(d.biome(), Biome::Forest);
}

TEST_F(DungeonTest, BSPHasWalkablePath) {
    Dungeon d;
    d.generate_bsp(Biome::Dungeon);
    int floor_count = 0;
    for (int y = 0; y < MAP_HEIGHT; ++y) {
        for (int x = 0; x < MAP_WIDTH; ++x) {
            if (d.is_walkable(x, y)) ++floor_count;
        }
    }
    EXPECT_GT(floor_count, 0);
}

TEST_F(DungeonTest, CellularGeneratesFloors) {
    Dungeon d;
    d.generate_cellular(Biome::Cave);
    int floor_count = 0;
    for (int y = 0; y < MAP_HEIGHT; ++y) {
        for (int x = 0; x < MAP_WIDTH; ++x) {
            if (d.is_walkable(x, y)) ++floor_count;
        }
    }
    EXPECT_GT(floor_count, 0);
}

TEST_F(DungeonTest, CellularBiome) {
    Dungeon d;
    d.generate_cellular(Biome::Cave);
    EXPECT_EQ(d.biome(), Biome::Cave);
}

TEST_F(DungeonTest, BSPMultipleRooms) {
    Dungeon d;
    d.generate_bsp(Biome::Dungeon);
    EXPECT_GE(d.rooms().size(), 1u);
    EXPECT_LE(d.rooms().size(), static_cast<size_t>(MAX_ROOMS));
}
