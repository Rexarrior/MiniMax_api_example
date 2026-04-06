#pragma once

#include "../core/types.h"

namespace rl {

enum class PortalType { Entry, Exit };

struct Portal {
    Position pos;
    PortalType type;
    bool active = true;
};

}
