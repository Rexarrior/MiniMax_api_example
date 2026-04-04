#include "entity.h"

namespace rl {

Entity::Entity(Position pos, EntityType type, const std::string& sprite_name)
    : pos_(pos), type_(type), sprite_name_(sprite_name) {}

}
