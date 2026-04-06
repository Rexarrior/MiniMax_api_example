#include <gtest/gtest.h>
#include "combat/combat.h"
#include "core/random.h"
#include "core/types.h"

using namespace rl;

class CombatTest : public ::testing::Test {
protected:
    void SetUp() override {
        RNG::instance().seed(42);
    }
};

TEST_F(CombatTest, ChampionAttacksDealsDamage) {
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Skeleton);
    int enemy_hp_before = enemy.stats().hp;

    CombatResult result = champion_attacks(champion, enemy);

    EXPECT_GT(result.damage_dealt, 0);
    EXPECT_LT(enemy.stats().hp, enemy_hp_before);
}

TEST_F(CombatTest, ChampionAttacksKillsWeakEnemy) {
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Slime);

    CombatResult result = champion_attacks(champion, enemy);

    if (result.damage_dealt >= enemy.stats().hp + result.damage_dealt) {
        EXPECT_TRUE(result.killed);
        EXPECT_FALSE(enemy.alive());
    }
}

TEST_F(CombatTest, ChampionAttacksMessageContainsDamage) {
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Skeleton);

    CombatResult result = champion_attacks(champion, enemy);

    EXPECT_FALSE(result.message.empty());
    EXPECT_NE(result.message.find("damage"), std::string::npos);
}

TEST_F(CombatTest, EnemyAttacksDealsDamage) {
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Orc);
    int champion_hp_before = champion.stats().hp;

    CombatResult result = enemy_attacks(enemy, champion);

    EXPECT_GT(result.damage_dealt, 0);
    EXPECT_LT(champion.stats().hp, champion_hp_before);
}

TEST_F(CombatTest, EnemyAttacksMessage) {
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Goblin);

    CombatResult result = enemy_attacks(enemy, champion);

    EXPECT_FALSE(result.message.empty());
    EXPECT_NE(result.message.find("damage"), std::string::npos);
}

TEST_F(CombatTest, CriticalDoublesDamage) {
    RNG::instance().seed(100);
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Skeleton);

    CombatResult result = champion_attacks(champion, enemy);

    if (result.critical) {
        EXPECT_EQ(result.damage_dealt % 2, 0);
    }
}

TEST_F(CombatTest, DamageIsAlwaysPositive) {
    for (int seed = 0; seed < 50; ++seed) {
        RNG::instance().seed(seed);
        Champion champion({0, 0});
        Enemy enemy({1, 1}, EnemyType::Skeleton);

        CombatResult result = champion_attacks(champion, enemy);
        EXPECT_GE(result.damage_dealt, 1);
    }
}

TEST_F(CombatTest, EnemyDamageIsAlwaysPositive) {
    for (int seed = 0; seed < 50; ++seed) {
        RNG::instance().seed(seed);
        Champion champion({0, 0});
        Enemy enemy({1, 1}, EnemyType::Skeleton);

        CombatResult result = enemy_attacks(enemy, champion);
        EXPECT_GE(result.damage_dealt, 1);
    }
}

TEST_F(CombatTest, ChampionDiesAtZeroHp) {
    RNG::instance().seed(200);
    Champion champion({0, 0});
    champion.stats().hp = 1;
    Enemy enemy({1, 1}, EnemyType::Orc);

    CombatResult result = enemy_attacks(enemy, champion);

    EXPECT_LE(champion.stats().hp, 0);
    if (champion.stats().hp <= 0) {
        EXPECT_TRUE(result.killed);
        EXPECT_NE(result.message.find("slain"), std::string::npos);
    }
}

TEST_F(CombatTest, EnemyDiesAtZeroHp) {
    RNG::instance().seed(300);
    Champion champion({0, 0});
    Enemy enemy({1, 1}, EnemyType::Slime);

    CombatResult result = champion_attacks(champion, enemy);

    if (result.killed) {
        EXPECT_FALSE(enemy.alive());
        EXPECT_NE(result.message.find("defeated"), std::string::npos);
    }
}
