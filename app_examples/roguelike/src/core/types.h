#pragma once

#include <string>
#include <vector>

namespace rl {

enum class Direction { None, Up, Down, Left, Right };

struct Position {
    int x = 0;
    int y = 0;
    bool operator==(const Position& o) const { return x == o.x && y == o.y; }
    bool operator!=(const Position& o) const { return !(*this == o); }
    Position operator+(const Position& o) const { return {x + o.x, y + o.y}; }
};

enum class TileType {
    Wall,
    Floor,
    Door,
    Wall_Torch,
    Floor_Water,
};

enum class Biome {
    Dungeon,
    Cave,
    Forest,
};

enum class EntityType {
    Champion,
    Enemy,
    Item,
    Portal,
};

enum class EnemyType {
    Skeleton,
    Goblin,
    Orc,
    GiantRat,
    GiantSpider,
    Slime,
    FireDemon,
    Ghost,
    Werewolf,
    DarkMage,
};

enum class GameState {
    Menu,
    Playing,
    Paused,
    GameOver,
    Victory,
    Inventory,
};

struct Stats {
    int hp = 10;
    int max_hp = 10;
    int attack = 3;
    int defense = 1;
    int speed = 1;
};

}
