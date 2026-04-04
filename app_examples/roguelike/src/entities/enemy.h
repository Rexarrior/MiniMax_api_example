#pragma once

#include "entity.h"
#include "../core/types.h"

namespace rl {

class Enemy : public Entity {
public:
    Enemy(Position pos, EnemyType type);

    EnemyType enemy_type() const { return enemy_type_; }
    int xp_value() const { return xp_value_; }

    void set_ai_state(int state) { ai_state_ = state; }
    int ai_state() const { return ai_state_; }

    static std::string sprite_name_for(EnemyType type);
    static Stats stats_for(EnemyType type);
    static int xp_for(EnemyType type);

private:
    EnemyType enemy_type_ = EnemyType::Skeleton;
    int xp_value_ = 5;
    int ai_state_ = 0;
};

}
