#include "enemy.h"

namespace rl {

Enemy::Enemy(Position pos, EnemyType type)
    : Entity(pos, EntityType::Enemy, sprite_name_for(type)),
      enemy_type_(type),
      xp_value_(xp_for(type)) {
    stats_ = stats_for(type);
}

std::string Enemy::sprite_name_for(EnemyType type) {
    switch (type) {
        case EnemyType::Skeleton:   return "skeleton";
        case EnemyType::Goblin:     return "goblin";
        case EnemyType::Orc:        return "orc";
        case EnemyType::GiantRat:   return "rat";
        case EnemyType::GiantSpider:return "spider";
        case EnemyType::Slime:      return "slime";
        case EnemyType::FireDemon:  return "demon";
        case EnemyType::Ghost:      return "ghost";
        case EnemyType::Werewolf:   return "werewolf";
        case EnemyType::DarkMage:   return "dark_mage";
    }
    return "skeleton";
}

Stats Enemy::stats_for(EnemyType type) {
    switch (type) {
        case EnemyType::Skeleton:   return {8, 8, 3, 1, 1};
        case EnemyType::Goblin:     return {6, 6, 2, 0, 2};
        case EnemyType::Orc:        return {18, 18, 6, 3, 1};
        case EnemyType::GiantRat:   return {4, 4, 2, 0, 2};
        case EnemyType::GiantSpider:return {5, 5, 3, 0, 2};
        case EnemyType::Slime:      return {3, 3, 1, 0, 1};
        case EnemyType::FireDemon:  return {25, 25, 8, 4, 1};
        case EnemyType::Ghost:      return {10, 10, 4, 1, 2};
        case EnemyType::Werewolf:   return {20, 20, 7, 2, 2};
        case EnemyType::DarkMage:   return {12, 12, 5, 1, 1};
    }
    return {5, 5, 2, 1, 1};
}

int Enemy::xp_for(EnemyType type) {
    switch (type) {
        case EnemyType::Skeleton:   return 5;
        case EnemyType::Goblin:     return 4;
        case EnemyType::Orc:        return 12;
        case EnemyType::GiantRat:   return 2;
        case EnemyType::GiantSpider:return 3;
        case EnemyType::Slime:      return 1;
        case EnemyType::FireDemon:  return 20;
        case EnemyType::Ghost:      return 8;
        case EnemyType::Werewolf:   return 15;
        case EnemyType::DarkMage:   return 10;
    }
    return 5;
}

}
