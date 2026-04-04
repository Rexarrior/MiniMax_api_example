cmake_minimum_required(VERSION 3.16)
project(roguelike LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(raylib REQUIRED)

set(SOURCES
    src/main.cpp
    src/game.cpp
    src/core/random.cpp
    src/assets/asset_manager.cpp
    src/assets/sprite_sheet.cpp
    src/map/dungeon.cpp
    src/map/generator.cpp
    src/map/cellular.cpp
    src/map/renderer.cpp
    src/entities/entity.cpp
    src/entities/champion.cpp
    src/entities/enemy.cpp
    src/entities/enemy_registry.cpp
    src/entities/item.cpp
    src/entities/portal.cpp
    src/ai/ai_system.cpp
    src/ai/behaviors.cpp
    src/combat/combat.cpp
    src/camera/camera.cpp
    src/ui/hud.cpp
    src/ui/message_log.cpp
    src/ui/menu.cpp
    src/systems/turn_manager.cpp
    src/systems/fov.cpp
    src/systems/particle.cpp
    src/input/input_handler.cpp
)

add_executable(roguelike ${SOURCES})
target_link_libraries(roguelike PRIVATE raylib)

if(MSVC)
    target_compile_options(roguelike PRIVATE /W4)
else()
    target_compile_options(roguelike PRIVATE -Wall -Wextra -Wpedantic)
endif()
