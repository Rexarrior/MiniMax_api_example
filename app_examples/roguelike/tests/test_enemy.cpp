#include <gtest/gtest.h>
#include "entities/enemy.h"
#include "core/types.h"

using namespace rl;

TEST(EnemyTest, SkeletonStats) {
    Enemy e({0, 0}, EnemyType::Skeleton);
    EXPECT_EQ(e.enemy_type(), EnemyType::Skeleton);
    EXPECT_EQ(e.xp_value(), 5);
    EXPECT_EQ(e.stats().hp, 8);
    EXPECT_EQ(e.stats().attack, 3);
    EXPECT_EQ(e.stats().defense, 1);
    EXPECT_EQ(e.sprite_name(), "skeleton");
}

TEST(EnemyTest, GoblinStats) {
    Enemy e({0, 0}, EnemyType::Goblin);
    EXPECT_EQ(e.xp_value(), 4);
    EXPECT_EQ(e.stats().hp, 6);
    EXPECT_EQ(e.stats().attack, 2);
    EXPECT_EQ(e.stats().defense, 0);
    EXPECT_EQ(e.stats().speed, 2);
    EXPECT_EQ(e.sprite_name(), "goblin");
}

TEST(EnemyTest, OrcStats) {
    Enemy e({0, 0}, EnemyType::Orc);
    EXPECT_EQ(e.xp_value(), 12);
    EXPECT_EQ(e.stats().hp, 18);
    EXPECT_EQ(e.stats().attack, 6);
    EXPECT_EQ(e.stats().defense, 3);
    EXPECT_EQ(e.sprite_name(), "orc");
}

TEST(EnemyTest, GiantRatStats) {
    Enemy e({0, 0}, EnemyType::GiantRat);
    EXPECT_EQ(e.xp_value(), 2);
    EXPECT_EQ(e.stats().hp, 4);
    EXPECT_EQ(e.stats().speed, 2);
    EXPECT_EQ(e.sprite_name(), "rat");
}

TEST(EnemyTest, GiantSpiderStats) {
    Enemy e({0, 0}, EnemyType::GiantSpider);
    EXPECT_EQ(e.xp_value(), 3);
    EXPECT_EQ(e.stats().hp, 5);
    EXPECT_EQ(e.stats().attack, 3);
    EXPECT_EQ(e.sprite_name(), "spider");
}

TEST(EnemyTest, SlimeStats) {
    Enemy e({0, 0}, EnemyType::Slime);
    EXPECT_EQ(e.xp_value(), 1);
    EXPECT_EQ(e.stats().hp, 3);
    EXPECT_EQ(e.stats().attack, 1);
    EXPECT_EQ(e.sprite_name(), "slime");
}

TEST(EnemyTest, FireDemonStats) {
    Enemy e({0, 0}, EnemyType::FireDemon);
    EXPECT_EQ(e.xp_value(), 20);
    EXPECT_EQ(e.stats().hp, 25);
    EXPECT_EQ(e.stats().attack, 8);
    EXPECT_EQ(e.stats().defense, 4);
    EXPECT_EQ(e.sprite_name(), "demon");
}

TEST(EnemyTest, GhostStats) {
    Enemy e({0, 0}, EnemyType::Ghost);
    EXPECT_EQ(e.xp_value(), 8);
    EXPECT_EQ(e.stats().hp, 10);
    EXPECT_EQ(e.stats().attack, 4);
    EXPECT_EQ(e.stats().defense, 1);
    EXPECT_EQ(e.stats().speed, 2);
    EXPECT_EQ(e.sprite_name(), "ghost");
}

TEST(EnemyTest, WerewolfStats) {
    Enemy e({0, 0}, EnemyType::Werewolf);
    EXPECT_EQ(e.xp_value(), 15);
    EXPECT_EQ(e.stats().hp, 20);
    EXPECT_EQ(e.stats().attack, 7);
    EXPECT_EQ(e.stats().defense, 2);
    EXPECT_EQ(e.stats().speed, 2);
    EXPECT_EQ(e.sprite_name(), "werewolf");
}

TEST(EnemyTest, DarkMageStats) {
    Enemy e({0, 0}, EnemyType::DarkMage);
    EXPECT_EQ(e.xp_value(), 10);
    EXPECT_EQ(e.stats().hp, 12);
    EXPECT_EQ(e.stats().attack, 5);
    EXPECT_EQ(e.stats().defense, 1);
    EXPECT_EQ(e.sprite_name(), "dark_mage");
}

TEST(EnemyTest, StaticStatsFor) {
    auto s = Enemy::stats_for(EnemyType::Skeleton);
    EXPECT_EQ(s.hp, 8);
    EXPECT_EQ(s.attack, 3);
    EXPECT_EQ(s.defense, 1);
}

TEST(EnemyTest, StaticXpFor) {
    EXPECT_EQ(Enemy::xp_for(EnemyType::Orc), 12);
    EXPECT_EQ(Enemy::xp_for(EnemyType::Slime), 1);
}

TEST(EnemyTest, StaticSpriteNameFor) {
    EXPECT_EQ(Enemy::sprite_name_for(EnemyType::FireDemon), "demon");
    EXPECT_EQ(Enemy::sprite_name_for(EnemyType::GiantSpider), "spider");
}

TEST(EnemyTest, Position) {
    Enemy e({7, 3}, EnemyType::Skeleton);
    EXPECT_EQ(e.pos().x, 7);
    EXPECT_EQ(e.pos().y, 3);
}

TEST(EnemyTest, AliveAndKill) {
    Enemy e({0, 0}, EnemyType::Skeleton);
    EXPECT_TRUE(e.alive());
    e.kill();
    EXPECT_FALSE(e.alive());
}

TEST(EnemyTest, AIState) {
    Enemy e({0, 0}, EnemyType::Skeleton);
    EXPECT_EQ(e.ai_state(), 0);
    e.set_ai_state(42);
    EXPECT_EQ(e.ai_state(), 42);
}
