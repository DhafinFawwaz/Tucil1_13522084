
#include "tokenslot.h"

struct TokenSlotData{
    Token token;
    int x;
    int y;
};

TokenSlot::TokenSlot(int length)
{
    bufferSize = length;
    slotList = new TokenSlotData[length];
    for(int i = 0; i < length; i++)
    {
        slotList[i].x = -1;
        slotList[i].y = -1;
    }
}
bool TokenSlot::indexHasBeenFilled(int i)
{
    return !(slotList[i].x == -1 || slotList[i].y == -1);
}


/// @brief Get total reward
/// @param sequence array of sequence containing its reward
/// @param sequenceAmount length of sequence
/// @return total reward based on sequence and this slotList
int TokenSlot::calculateReward(Sequence sequence[], int sequenceAmount)
{
    int totalReward = 0;
    for(int i = 0; i < sequenceAmount; i++)
    {
        totalReward += getReward(sequence[i]);
    }
    return totalReward;
}

/// @brief get reward
/// @param sequence the sequence (has reward) to check inside slot
/// @return 0 if the sequence doesn't exist in the slot. sequence.reward if its found. 
int TokenSlot::getReward(Sequence sequence)
{
    // loop through slot
    for(int i = 0; i < bufferSize - sequence.count + 1; i++)
    {
        // check the first element of sequence that's equal
        if(slotList[i].token == sequence.buffer[0])
        {
            // Check equal, just start from 1, because 0 is already checked
            bool isAlwaysEqual = true;
            for(int j = 1; j < sequence.count; j++)
            {
                if(slotList[i+j].token != sequence.buffer[j])
                {
                    isAlwaysEqual = false;
                    break;
                }
            }
            // if always equal, meaning found, return reward
            if(isAlwaysEqual) return sequence.reward;
        }
    }
    return 0;
}

void TokenSlot::CopyFrom(TokenSlot slot)
{
    bufferSize = slot.bufferSize;
    for(int i = 0; i < bufferSize; i++)
    {
        slotList[i].token = slot.slotList[i].token;
        slotList[i].x = slot.slotList[i].x;
        slotList[i].y = slot.slotList[i].y;
    }
}

void TokenSlot::Debug()
{
    cout << "[ ";
    for(int i = 0; i < bufferSize; i++)
    {
        cout << slotList[i].token << " ";
    }
    cout << "]" << endl;
    cout << "[ ";
    for(int i = 0; i < bufferSize; i++)
    {
        cout << '(' << slotList[i].y << ", " << slotList[i].x << ") ";
    }
    cout << "]" << endl;
}
