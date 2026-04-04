#include "particle.h"
#include "../core/random.h"
#include <algorithm>

namespace rl {

void ParticleSystem::emit(float x, float y, Color color, int count) {
    auto& rng = RNG::instance();
    for (int i = 0; i < count; ++i) {
        Particle p;
        p.x = x;
        p.y = y;
        p.vx = rng.range(-60.0f, 60.0f);
        p.vy = rng.range(-80.0f, -20.0f);
        p.life = rng.range(0.3f, 0.8f);
        p.max_life = p.life;
        p.color = color;
        particles_.push_back(p);
    }
}

void ParticleSystem::update(float dt) {
    for (auto& p : particles_) {
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.vy += 120.0f * dt;
        p.life -= dt;
    }
    particles_.erase(
        std::remove_if(particles_.begin(), particles_.end(),
                       [](const Particle& p) { return p.life <= 0; }),
        particles_.end());
}

void ParticleSystem::render() const {
    for (const auto& p : particles_) {
        float alpha = p.life / p.max_life;
        Color c = {p.color.r, p.color.g, p.color.b, static_cast<unsigned char>(alpha * 255)};
        DrawRectangle(static_cast<int>(p.x), static_cast<int>(p.y), 2, 2, c);
    }
}

}
