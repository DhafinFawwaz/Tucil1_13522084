
#ifndef TOKENSLOT_H
#define TOKENSLOT_H

#include "sequence.h"

struct TokenSlot{
    struct TokenSlotData{
        Token token;
        int x;
        int y;
    };

    int filledSlot;
    int bufferSize;
    TokenSlotData* slotList;

    TokenSlot(int length);
    bool indexHasBeenFilled(int i);


    /// @brief Get total reward
    /// @param sequence array of sequence containing its reward
    /// @param sequenceAmount length of sequence
    /// @return total reward based on sequence and this slotList
    int calculateReward(Sequence sequence[], int sequenceAmount);

    /// @brief get reward
    /// @param sequence the sequence (has reward) to check inside slot
    /// @return 0 if the sequence doesn't exist in the slot. sequence.reward if its found. 
    int getReward(Sequence sequence);
    int getReward_v2(Sequence sequence, int maxIdxTocheck);
    void CopyFrom(TokenSlot slot);
    void Debug();
};


#endif