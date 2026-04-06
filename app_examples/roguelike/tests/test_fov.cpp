#include <gtest/gtest.h>
#include "systems/fov.h"
#include "map/dungeon.h"
#include "core/config.h"
#include "core/random.h"

using namespace rl;

class FOVTest : public ::testing::Test {
protected:
    void SetUp() override {
        RNG::instance().seed(42);
    }
};

TEST_F(FOVTest, CenterTileAlwaysVisible) {
    Dungeon d;
    d.set_tile(20, 12, TileType::Floor);

    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_TRUE(fov.is_visible(20, 12));
    EXPECT_TRUE(fov.is_explored(20, 12));
}

TEST_F(FOVTest, WallsBlockVisibility) {
    Dungeon d;
    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            d.set_tile(x, y, TileType::Floor);

    d.set_tile(25, 12, TileType::Wall);
    d.set_tile(25, 11, TileType::Wall);
    d.set_tile(25, 13, TileType::Wall);

    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_TRUE(fov.is_visible(24, 12));
    EXPECT_FALSE(fov.is_visible(26, 12));
}

TEST_F(FOVTest, ExploredTilesStayExplored) {
    Dungeon d;
    d.set_tile(20, 12, TileType::Floor);
    d.set_tile(21, 12, TileType::Floor);

    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);
    EXPECT_TRUE(fov.is_explored(21, 12));

    fov.compute(d, 20, 12, FOV_RADIUS);
    EXPECT_TRUE(fov.is_explored(21, 12));
}

TEST_F(FOVTest, OutOfBoundsNotVisible) {
    Dungeon d;
    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_FALSE(fov.is_visible(-1, 0));
    EXPECT_FALSE(fov.is_visible(MAP_WIDTH, 0));
    EXPECT_FALSE(fov.is_visible(0, -1));
    EXPECT_FALSE(fov.is_visible(0, MAP_HEIGHT));
}

TEST_F(FOVTest, OutOfBoundsNotExplored) {
    Dungeon d;
    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_FALSE(fov.is_explored(-1, 0));
    EXPECT_FALSE(fov.is_explored(MAP_WIDTH, 0));
    EXPECT_FALSE(fov.is_explored(0, -1));
    EXPECT_FALSE(fov.is_explored(0, MAP_HEIGHT));
}

TEST_F(FOVTest, AdjacentFloorVisible) {
    Dungeon d;
    d.set_tile(20, 12, TileType::Floor);
    d.set_tile(21, 12, TileType::Floor);

    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_TRUE(fov.is_visible(21, 12));
}

TEST_F(FOVTest, DistantNotVisible) {
    Dungeon d;
    d.set_tile(20, 12, TileType::Floor);
    d.set_tile(35, 12, TileType::Floor);

    FOV fov;
    fov.compute(d, 20, 12, 5);

    EXPECT_FALSE(fov.is_visible(35, 12));
}

TEST_F(FOVTest, BSPDungeonFOV) {
    Dungeon d;
    d.generate_bsp(Biome::Dungeon);

    FOV fov;
    fov.compute(d, 20, 12, FOV_RADIUS);

    EXPECT_TRUE(fov.is_visible(20, 12));
    EXPECT_TRUE(fov.is_explored(20, 12));
}
