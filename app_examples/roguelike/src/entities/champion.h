#pragma once

#include "entity.h"
#include <vector>
#include <string>

namespace rl {

class Champion : public Entity {
public:
    Champion(Position pos);

    void move(Direction dir);
    int xp() const { return xp_; }
    int level() const { return level_; }
    int floor() const { return floor_; }
    void set_floor(int f) { floor_ = f; }

    void gain_xp(int amount);
    bool has_potions() const { return potions_ > 0; }
    void use_potion();
    int potions() const { return potions_; }
    void add_potion() { ++potions_; }

private:
    int xp_ = 0;
    int level_ = 1;
    int floor_ = 1;
    int potions_ = 1;
};

}
