#pragma once

/*
 * Minimal raylib stub for unit testing.
 * Provides only the types / constants that the roguelike project
 * transitively needs when compiling without a real display context.
 */

#ifdef USE_RAYLIB_STUB

/* ── basic types ─────────────────────────────────────────────── */

typedef struct Vector2 { float x; float y; } Vector2;

typedef struct Vector3 { float x; float y; float z; } Vector3;

typedef struct Rectangle { float x; float y; float width; float height; } Rectangle;

typedef struct Color { unsigned char r; unsigned char g; unsigned char b; unsigned char a; } Color;

typedef struct Texture2D { unsigned int id; int width; int height; int mipmaps; int format; } Texture2D;

typedef struct Camera2D { Vector2 offset; Vector2 target; float rotation; float zoom; } Camera2D;

typedef struct Image { void* data; int width; int height; int mipmaps; int format; } Image;

typedef struct Font { int baseSize; int glyphCount; int glyphPadding; Texture2D texture; void* recs; void* chars; } Font;

typedef struct Ray { Vector3 position; Vector3 direction; } Ray;

typedef struct RayHitInfo { bool hit; float distance; Vector3 position; Vector3 normal; } RayHitInfo;

typedef struct BoundingBox { Vector3 min; Vector3 max; } BoundingBox;

typedef struct Matrix { float m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15; } Matrix;

typedef struct VRDeviceInfo { int hResolution; int vResolution; float hScreenSize; float vScreenSize; float vScreenCenter; float eyeToScreenDistance; float lensSeparationDistance; float interpupillaryDistance; float lensDistortionValues[4]; float chromaAbCorrection[4]; } VRDeviceInfo;

typedef struct VrStereoConfig { Matrix projection[2]; Matrix viewOffset[2]; float leftLensCenter[2]; float rightLensCenter[2]; float leftScreenCenter[2]; float rightScreenCenter[2]; float scale[2]; float scaleIn[2]; } VrStereoConfig;

/* ── colours ─────────────────────────────────────────────────── */

static const Color LIGHTGRAY  = { 200, 200, 200, 255 };
static const Color GRAY       = { 130, 130, 130, 255 };
static const Color DARKGRAY   = { 80, 80, 80, 255 };
static const Color YELLOW     = { 253, 249, 0, 255 };
static const Color GOLD       = { 255, 203, 0, 255 };
static const Color ORANGE     = { 255, 161, 0, 255 };
static const Color PINK       = { 255, 109, 194, 255 };
static const Color RED        = { 230, 41, 55, 255 };
static const Color MAROON     = { 190, 33, 55, 255 };
static const Color GREEN      = { 0, 228, 48, 255 };
static const Color LIME       = { 0, 158, 47, 255 };
static const Color DARKGREEN  = { 0, 117, 44, 255 };
static const Color SKYBLUE    = { 102, 191, 255, 255 };
static const Color BLUE       = { 0, 121, 241, 255 };
static const Color DARKBLUE   = { 0, 82, 172, 255 };
static const Color PURPLE     = { 200, 122, 255, 255 };
static const Color VIOLET     = { 135, 60, 190, 255 };
static const Color DARKPURPLE = { 112, 31, 126, 255 };
static const Color BEIGE      = { 211, 176, 131, 255 };
static const Color BROWN      = { 127, 106, 79, 255 };
static const Color DARKBROWN  = { 76, 63, 47, 255 };

static const Color WHITE      = { 255, 255, 255, 255 };
static const Color BLACK      = { 0, 0, 0, 255 };
static const Color BLANK      = { 0, 0, 0, 0 };
static const Color MAGENTA    = { 255, 0, 255, 255 };

/* ── keyboard / mouse / gamepad enums (minimal) ──────────────── */

typedef enum KeyboardKey { KEY_NULL = 0, KEY_SPACE = 32, KEY_ESCAPE = 256, KEY_ENTER = 257, KEY_LEFT = 263, KEY_RIGHT = 262, KEY_UP = 265, KEY_DOWN = 264, KEY_A = 65, KEY_D = 68, KEY_E = 69, KEY_I = 73, KEY_P = 80, KEY_Q = 81, KEY_R = 82, KEY_S = 83, KEY_W = 87 } KeyboardKey;

typedef enum MouseButton { MOUSE_LEFT_BUTTON = 0, MOUSE_RIGHT_BUTTON = 1, MOUSE_MIDDLE_BUTTON = 2 } MouseButton;

typedef enum GamepadButton { GAMEPAD_BUTTON_UNKNOWN = 0 } GamepadButton;

typedef enum GamepadAxis { GAMEPAD_AXIS_LEFT_X = 0, GAMEPAD_AXIS_LEFT_Y = 1, GAMEPAD_AXIS_RIGHT_X = 2, GAMEPAD_AXIS_RIGHT_Y = 3, GAMEPAD_AXIS_LEFT_TRIGGER = 4, GAMEPAD_AXIS_RIGHT_TRIGGER = 5 } GamepadAxis;

/* ── stub functions (no-ops or minimal) ──────────────────────── */

#ifdef __cplusplus
extern "C" {
#endif

static inline void InitWindow(int w, int h, const char* title) { (void)w; (void)h; (void)title; }
static inline void CloseWindow(void) {}
static inline bool WindowShouldClose(void) { return 0; }
static inline bool IsKeyDown(KeyboardKey key) { (void)key; return 0; }
static inline bool IsKeyPressed(KeyboardKey key) { (void)key; return 0; }
static inline bool IsMouseButtonPressed(MouseButton button) { (void)button; return 0; }
static inline int GetMouseX(void) { return 0; }
static inline int GetMouseY(void) { return 0; }
static inline Vector2 GetMousePosition(void) { return (Vector2){0, 0}; }
static inline void BeginDrawing(void) {}
static inline void EndDrawing(void) {}
static inline void ClearBackground(Color color) { (void)color; }
static inline void DrawText(const char* text, int posX, int posY, int fontSize, Color color) { (void)text; (void)posX; (void)posY; (void)fontSize; (void)color; }
static inline void DrawRectangle(int posX, int posY, int width, int height, Color color) { (void)posX; (void)posY; (void)width; (void)height; (void)color; }
static inline void DrawRectangleRec(Rectangle rec, Color color) { (void)rec; (void)color; }
static inline void DrawTexture(Texture2D texture, int posX, int posY, Color tint) { (void)texture; (void)posX; (void)posY; (void)tint; }
static inline void DrawTextureRec(Texture2D texture, Rectangle sourceRec, Vector2 position, Color tint) { (void)texture; (void)sourceRec; (void)position; (void)tint; }
static inline void DrawTexturePro(Texture2D texture, Rectangle sourceRec, Rectangle destRec, Vector2 origin, float rotation, Color tint) { (void)texture; (void)sourceRec; (void)destRec; (void)origin; (void)rotation; (void)tint; }
static inline void DrawFPS(int posX, int posY) { (void)posX; (void)posY; }
static inline void SetTargetFPS(int fps) { (void)fps; }
static inline int GetFPS(void) { return 60; }
static inline float GetFrameTime(void) { return 1.0f/60.0f; }
static inline Texture2D LoadTexture(const char* fileName) { (void)fileName; Texture2D t = {0}; return t; }
static inline void UnloadTexture(Texture2D texture) { (void)texture; }
static inline Font LoadFont(const char* fileName) { (void)fileName; Font f = {0}; return f; }
static inline void UnloadFont(Font font) { (void)font; }
static inline Image LoadImage(const char* fileName) { (void)fileName; Image i = {0}; return i; }
static inline void UnloadImage(Image image) { (void)image; }
static inline int GetKeyPressed(void) { return 0; }
static inline void SetExitKey(int key) { (void)key; }
static inline bool IsGamepadAvailable(int gamepad) { (void)gamepad; return 0; }
static inline int GetGamepadButtonPressed(void) { return 0; }
static inline int GetGamepadAxisMovement(int gamepad, GamepadAxis axis) { (void)gamepad; (void)axis; return 0; }
static inline float MeasureText(const char* text, int fontSize) { (void)text; (void)fontSize; return 0; }
static inline void DrawLine(int startPosX, int startPosY, int endPosX, int endPosY, Color color) { (void)startPosX; (void)startPosY; (void)endPosX; (void)endPosY; (void)color; }
static inline void DrawCircle(int centerX, int centerY, float radius, Color color) { (void)centerX; (void)centerY; (void)radius; (void)color; }
static inline void BeginMode2D(Camera2D camera) { (void)camera; }
static inline void EndMode2D(void) {}
static inline Vector2 GetWorldToScreen2D(Vector2 position, Camera2D camera) { (void)position; (void)camera; return position; }
static inline Vector2 GetScreenToWorld2D(Vector2 position, Camera2D camera) { (void)position; (void)camera; return position; }

#ifdef __cplusplus
}
#endif

#endif /* USE_RAYLIB_STUB */
