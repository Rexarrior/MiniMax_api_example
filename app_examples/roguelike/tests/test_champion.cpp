#include <gtest/gtest.h>
#include "entities/champion.h"
#include "core/types.h"

using namespace rl;

TEST(ChampionTest, InitialStats) {
    Champion c({0, 0});
    EXPECT_EQ(c.level(), 1);
    EXPECT_EQ(c.xp(), 0);
    EXPECT_EQ(c.floor(), 1);
    EXPECT_EQ(c.stats().hp, 30);
    EXPECT_EQ(c.stats().max_hp, 30);
    EXPECT_EQ(c.stats().attack, 5);
    EXPECT_EQ(c.stats().defense, 3);
    EXPECT_TRUE(c.alive());
    EXPECT_TRUE(c.has_potions());
    EXPECT_EQ(c.potions(), 1);
}

TEST(ChampionTest, MoveUp) {
    Champion c({5, 5});
    c.move(Direction::Up);
    EXPECT_EQ(c.pos().x, 5);
    EXPECT_EQ(c.pos().y, 4);
}

TEST(ChampionTest, MoveDown) {
    Champion c({5, 5});
    c.move(Direction::Down);
    EXPECT_EQ(c.pos().x, 5);
    EXPECT_EQ(c.pos().y, 6);
}

TEST(ChampionTest, MoveLeft) {
    Champion c({5, 5});
    c.move(Direction::Left);
    EXPECT_EQ(c.pos().x, 4);
    EXPECT_EQ(c.pos().y, 5);
}

TEST(ChampionTest, MoveRight) {
    Champion c({5, 5});
    c.move(Direction::Right);
    EXPECT_EQ(c.pos().x, 6);
    EXPECT_EQ(c.pos().y, 5);
}

TEST(ChampionTest, MoveNone) {
    Champion c({5, 5});
    c.move(Direction::None);
    EXPECT_EQ(c.pos().x, 5);
    EXPECT_EQ(c.pos().y, 5);
}

TEST(ChampionTest, GainXpNoLevelUp) {
    Champion c({0, 0});
    c.gain_xp(5);
    EXPECT_EQ(c.xp(), 5);
    EXPECT_EQ(c.level(), 1);
}

TEST(ChampionTest, GainXpLevelUp) {
    Champion c({0, 0});
    c.gain_xp(15);
    EXPECT_EQ(c.level(), 2);
    EXPECT_EQ(c.stats().max_hp, 35);
    EXPECT_EQ(c.stats().hp, 35);
    EXPECT_EQ(c.stats().attack, 6);
    EXPECT_EQ(c.stats().defense, 4);
}

TEST(ChampionTest, GainXpMultipleLevels) {
    Champion c({0, 0});
    c.gain_xp(45);
    EXPECT_EQ(c.level(), 3);
}

TEST(ChampionTest, UsePotion) {
    Champion c({0, 0});
    c.stats().hp = 10;
    c.use_potion();
    EXPECT_EQ(c.stats().hp, 25);
    EXPECT_EQ(c.potions(), 0);
    EXPECT_FALSE(c.has_potions());
}

TEST(ChampionTest, UsePotionNoPotions) {
    Champion c({0, 0});
    c.stats().hp = 10;
    c.use_potion();
    c.use_potion();
    EXPECT_EQ(c.stats().hp, 25);
    EXPECT_EQ(c.potions(), 0);
}

TEST(ChampionTest, UsePotionAtFullHp) {
    Champion c({0, 0});
    c.use_potion();
    EXPECT_EQ(c.stats().hp, 30);
    EXPECT_EQ(c.potions(), 0);
}

TEST(ChampionTest, SetFloor) {
    Champion c({0, 0});
    c.set_floor(5);
    EXPECT_EQ(c.floor(), 5);
}

TEST(ChampionTest, AddPotion) {
    Champion c({0, 0});
    c.use_potion();
    EXPECT_EQ(c.potions(), 0);
    c.add_potion();
    EXPECT_EQ(c.potions(), 1);
    EXPECT_TRUE(c.has_potions());
}
