#include <gtest/gtest.h>
#include "core/types.h"

using namespace rl;

TEST(PositionTest, DefaultConstructor) {
    Position p;
    EXPECT_EQ(p.x, 0);
    EXPECT_EQ(p.y, 0);
}

TEST(PositionTest, Equality) {
    Position a{3, 4};
    Position b{3, 4};
    Position c{3, 5};
    EXPECT_EQ(a, b);
    EXPECT_NE(a, c);
}

TEST(PositionTest, Inequality) {
    Position a{0, 0};
    Position b{1, 0};
    Position c{0, 1};
    Position d{1, 1};
    EXPECT_NE(a, b);
    EXPECT_NE(a, c);
    EXPECT_NE(a, d);
}

TEST(PositionTest, Addition) {
    Position a{3, 4};
    Position b{1, 2};
    Position result = a + b;
    EXPECT_EQ(result.x, 4);
    EXPECT_EQ(result.y, 6);
}

TEST(PositionTest, AdditionWithNegative) {
    Position a{5, 5};
    Position b{-2, -3};
    Position result = a + b;
    EXPECT_EQ(result.x, 3);
    EXPECT_EQ(result.y, 2);
}

TEST(PositionTest, AdditionWithZero) {
    Position a{7, 8};
    Position b{0, 0};
    Position result = a + b;
    EXPECT_EQ(result, a);
}

TEST(StatsTest, DefaultValues) {
    Stats s;
    EXPECT_EQ(s.hp, 10);
    EXPECT_EQ(s.max_hp, 10);
    EXPECT_EQ(s.attack, 3);
    EXPECT_EQ(s.defense, 1);
    EXPECT_EQ(s.speed, 1);
}

TEST(DirectionTest, EnumValues) {
    EXPECT_EQ(static_cast<int>(Direction::None), 0);
    EXPECT_EQ(static_cast<int>(Direction::Up), 1);
    EXPECT_EQ(static_cast<int>(Direction::Down), 2);
    EXPECT_EQ(static_cast<int>(Direction::Left), 3);
    EXPECT_EQ(static_cast<int>(Direction::Right), 4);
}

TEST(TileTypeTest, EnumValues) {
    EXPECT_EQ(static_cast<int>(TileType::Wall), 0);
    EXPECT_EQ(static_cast<int>(TileType::Floor), 1);
    EXPECT_EQ(static_cast<int>(TileType::Door), 2);
    EXPECT_EQ(static_cast<int>(TileType::Wall_Torch), 3);
    EXPECT_EQ(static_cast<int>(TileType::Floor_Water), 4);
}

TEST(BiomeTest, EnumValues) {
    EXPECT_EQ(static_cast<int>(Biome::Dungeon), 0);
    EXPECT_EQ(static_cast<int>(Biome::Cave), 1);
    EXPECT_EQ(static_cast<int>(Biome::Forest), 2);
}

TEST(EnemyTypeTest, EnumValues) {
    EXPECT_EQ(static_cast<int>(EnemyType::Skeleton), 0);
    EXPECT_EQ(static_cast<int>(EnemyType::Goblin), 1);
    EXPECT_EQ(static_cast<int>(EnemyType::Orc), 2);
    EXPECT_EQ(static_cast<int>(EnemyType::GiantRat), 3);
    EXPECT_EQ(static_cast<int>(EnemyType::GiantSpider), 4);
    EXPECT_EQ(static_cast<int>(EnemyType::Slime), 5);
    EXPECT_EQ(static_cast<int>(EnemyType::FireDemon), 6);
    EXPECT_EQ(static_cast<int>(EnemyType::Ghost), 7);
    EXPECT_EQ(static_cast<int>(EnemyType::Werewolf), 8);
    EXPECT_EQ(static_cast<int>(EnemyType::DarkMage), 9);
}

TEST(GameStateTest, EnumValues) {
    EXPECT_EQ(static_cast<int>(GameState::Menu), 0);
    EXPECT_EQ(static_cast<int>(GameState::Playing), 1);
    EXPECT_EQ(static_cast<int>(GameState::Paused), 2);
    EXPECT_EQ(static_cast<int>(GameState::GameOver), 3);
    EXPECT_EQ(static_cast<int>(GameState::Victory), 4);
    EXPECT_EQ(static_cast<int>(GameState::Inventory), 5);
}
