#pragma once

#include "raylib.h"
#include <vector>

namespace rl {

struct Particle {
    float x, y;
    float vx, vy;
    float life;
    float max_life;
    Color color;
};

class ParticleSystem {
public:
    void emit(float x, float y, Color color, int count = 5);
    void update(float dt);
    void render() const;

private:
    std::vector<Particle> particles_;
};

}
