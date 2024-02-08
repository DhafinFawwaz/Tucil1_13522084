#ifndef CRACKDATA_H
#define CRACKDATA_H

#include "tokenslot.h"

/// @brief Can be used to pass data outside dll
struct CrackData{
    TokenSlot mostRewardingSlot;
    int maxReward;
    int executionDuration;
};

#endif