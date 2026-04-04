#include <gtest/gtest.h>
#include "core/random.h"
#include <set>
#include <algorithm>

using namespace rl;

class RNGTest : public ::testing::Test {
protected:
    void SetUp() override {
        RNG::instance().seed(42);
    }
};

TEST_F(RNGTest, RangeIntBounds) {
    for (int i = 0; i < 100; ++i) {
        int val = RNG::instance().range(5, 10);
        EXPECT_GE(val, 5);
        EXPECT_LE(val, 10);
    }
}

TEST_F(RNGTest, RangeIntSingleValue) {
    int val = RNG::instance().range(7, 7);
    EXPECT_EQ(val, 7);
}

TEST_F(RNGTest, RangeFloatBounds) {
    for (int i = 0; i < 100; ++i) {
        float val = RNG::instance().range(1.0f, 5.0f);
        EXPECT_GE(val, 1.0f);
        EXPECT_LE(val, 5.0f);
    }
}

TEST_F(RNGTest, RangeIntProducesVariety) {
    std::set<int> values;
    for (int i = 0; i < 200; ++i) {
        values.insert(RNG::instance().range(0, 9));
    }
    EXPECT_GE(values.size(), 5u);
}

TEST_F(RNGTest, ChanceZeroAlwaysFalse) {
    RNG::instance().seed(123);
    for (int i = 0; i < 100; ++i) {
        EXPECT_FALSE(RNG::instance().chance(0.0f));
    }
}

TEST_F(RNGTest, ChanceHundredAlwaysTrue) {
    RNG::instance().seed(456);
    for (int i = 0; i < 100; ++i) {
        EXPECT_TRUE(RNG::instance().chance(100.0f));
    }
}

TEST_F(RNGTest, ChanceDistribution) {
    RNG::instance().seed(789);
    int successes = 0;
    int trials = 1000;
    for (int i = 0; i < trials; ++i) {
        if (RNG::instance().chance(50.0f)) {
            ++successes;
        }
    }
    EXPECT_GE(successes, 400);
    EXPECT_LE(successes, 600);
}

TEST_F(RNGTest, PickFromVector) {
    RNG::instance().seed(100);
    std::vector<int> vec = {10, 20, 30, 40, 50};
    for (int i = 0; i < 50; ++i) {
        int val = RNG::instance().pick(vec);
        EXPECT_TRUE(val == 10 || val == 20 || val == 30 || val == 40 || val == 50);
    }
}

TEST_F(RNGTest, PickProducesAllElements) {
    RNG::instance().seed(200);
    std::vector<std::string> vec = {"a", "b", "c"};
    std::set<std::string> picked;
    for (int i = 0; i < 100; ++i) {
        picked.insert(RNG::instance().pick(vec));
    }
    EXPECT_EQ(picked.size(), 3u);
}

TEST_F(RNGTest, SeededReproducibility) {
    RNG::instance().seed(999);
    std::vector<int> first;
    for (int i = 0; i < 10; ++i) first.push_back(RNG::instance().range(0, 100));

    RNG::instance().seed(999);
    std::vector<int> second;
    for (int i = 0; i < 10; ++i) second.push_back(RNG::instance().range(0, 100));

    EXPECT_EQ(first, second);
}
