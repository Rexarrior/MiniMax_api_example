#include <gtest/gtest.h>
#include "entities/item.h"
#include "core/types.h"

using namespace rl;

TEST(ItemTest, MakePotion) {
    Position pos{3, 4};
    Item item = Item::make_potion(pos);
    EXPECT_EQ(item.pos, pos);
    EXPECT_EQ(item.type, ItemType::HealthPotion);
    EXPECT_EQ(item.name, "Health Potion");
    EXPECT_EQ(item.value, 15);
    EXPECT_FALSE(item.picked_up);
}

TEST(ItemTest, MakeGold) {
    Position pos{10, 20};
    Item item = Item::make_gold(pos, 50);
    EXPECT_EQ(item.pos, pos);
    EXPECT_EQ(item.type, ItemType::Gold);
    EXPECT_EQ(item.name, "Gold");
    EXPECT_EQ(item.value, 50);
    EXPECT_FALSE(item.picked_up);
}

TEST(ItemTest, MakeGoldZero) {
    Position pos{0, 0};
    Item item = Item::make_gold(pos, 0);
    EXPECT_EQ(item.value, 0);
}

TEST(ItemTest, MakeGoldLargeAmount) {
    Position pos{1, 1};
    Item item = Item::make_gold(pos, 999);
    EXPECT_EQ(item.value, 999);
}
