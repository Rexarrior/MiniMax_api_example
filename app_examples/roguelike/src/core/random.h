#pragma once

#include <random>

namespace rl {

class RNG {
public:
    static RNG& instance() {
        static RNG inst;
        return inst;
    }

    void seed(unsigned int s) { gen_.seed(s); }
    void seed_random() { gen_.seed(std::random_device{}()); }

    int range(int min, int max) {
        std::uniform_int_distribution<int> dist(min, max);
        return dist(gen_);
    }

    float range(float min, float max) {
        std::uniform_real_distribution<float> dist(min, max);
        return dist(gen_);
    }

    bool chance(float percent) {
        return range(0.0f, 100.0f) < percent;
    }

    template<typename T>
    const T& pick(const std::vector<T>& vec) {
        return vec[range(0, static_cast<int>(vec.size()) - 1)];
    }

private:
    RNG() { seed_random(); }
    std::mt19937 gen_;
};

}
