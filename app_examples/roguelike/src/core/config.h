#pragma once

namespace rl {

constexpr int SCREEN_WIDTH = 1280;
constexpr int SCREEN_HEIGHT = 720;
constexpr int TARGET_FPS = 60;

constexpr int TILE_SIZE = 128;
constexpr int MAP_WIDTH = 20;
constexpr int MAP_HEIGHT = 12;

constexpr int VIEWPORT_TILES_X = SCREEN_WIDTH / TILE_SIZE;
constexpr int VIEWPORT_TILES_Y = (SCREEN_HEIGHT - 64) / TILE_SIZE;

constexpr int MAX_ROOMS = 12;
constexpr int MIN_ROOM_SIZE = 6;
constexpr int MAX_ROOM_SIZE = 14;

constexpr int FOV_RADIUS = 10;

constexpr float TURN_DELAY = 0.15f;

}
