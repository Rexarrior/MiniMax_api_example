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

# ── Tests ──────────────────────────────────────────────────────────
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

set(TEST_SOURCES
    tests/test_types.cpp
    tests/test_random.cpp
    tests/test_dungeon.cpp
    tests/test_champion.cpp
    tests/test_enemy.cpp
    tests/test_item.cpp
    tests/test_combat.cpp
    tests/test_fov.cpp
    src/map/dungeon.cpp
    src/entities/champion.cpp
    src/entities/enemy.cpp
    src/entities/entity.cpp
    src/entities/item.cpp
    src/combat/combat.cpp
    src/systems/fov.cpp
    src/core/random.cpp
)

add_executable(roguelike_tests ${TEST_SOURCES})
target_include_directories(roguelike_tests PRIVATE ${CMAKE_SOURCE_DIR}/tests ${CMAKE_SOURCE_DIR}/src)
target_compile_definitions(roguelike_tests PRIVATE USE_RAYLIB_STUB)
target_link_libraries(roguelike_tests PRIVATE gtest gtest_main)

if(MSVC)
    target_compile_options(roguelike_tests PRIVATE /W4)
else()
    target_compile_options(roguelike_tests PRIVATE -Wall -Wextra -Wpedantic)
endif()

include(GoogleTest)
gtest_discover_tests(roguelike_tests)
