#include "cracker.h"
using namespace std;

void recursion(
    MarkableToken** matrix, int width, int height, 
    TokenSlot slot, int currentSlotIdx, 
    bool isHorizontal, 
    int* maxReward, 
    Sequence sequence[], int sequenceLength, 
    int posX, int posY,
    TokenSlot* mostRewardingSlot)
{

    // base case
    // khusus for loop paling dalam, atau slot paling kanan
    if(currentSlotIdx == slot.bufferSize)
    {      
        slot.filledSlot = currentSlotIdx;
        int currentTotalReward = slot.calculateReward(sequence, sequenceLength);
        if(currentTotalReward > *maxReward)
        {
            mostRewardingSlot->CopyFrom(slot);
            *maxReward = currentTotalReward;
        }

        return;
    }

    // isHorizontal udah direverse pas fungsi rekursinya dipanggil
    if(isHorizontal)
    {
        for(int j = 0; j < width; j++)
        {
            if(matrix[posY][j].isMarked) continue;

            // everytime a new mark is set, the previous needs to be unset. Like swapping
            // indexHasBeenFilled just to make sure the value is initialized
            if(slot.indexHasBeenFilled(currentSlotIdx))
                matrix[slot.slotList[currentSlotIdx].y][slot.slotList[currentSlotIdx].x].isMarked = false;
            
            posX = j;
            slot.slotList[currentSlotIdx].token = matrix[posY][posX].token;
            slot.slotList[currentSlotIdx].x = posX;
            slot.slotList[currentSlotIdx].y = posY;
            matrix[posY][posX].isMarked = true;
            recursion(
                matrix, width, height,
                slot, currentSlotIdx+1,
                !isHorizontal,
                maxReward,
                sequence, sequenceLength,
                posX, posY,
                mostRewardingSlot
            );
        }
    }
    else
    {
        for(int i = 0; i < height; i++)
        {
            if(matrix[i][posX].isMarked) continue;

            // everytime a new mark is set, the previous needs to be unset. Like swapping
            // happens when backtracking
            if(slot.indexHasBeenFilled(currentSlotIdx))
                matrix[slot.slotList[currentSlotIdx].y][slot.slotList[currentSlotIdx].x].isMarked = false;
            
            posY = i;
            slot.slotList[currentSlotIdx].token = matrix[posY][posX].token;
            slot.slotList[currentSlotIdx].x = posX;
            slot.slotList[currentSlotIdx].y = posY;
            matrix[posY][posX].isMarked = true;
            recursion(
                matrix, width, height,
                slot, currentSlotIdx+1,
                !isHorizontal,
                maxReward,
                sequence, sequenceLength,
                posX, posY,
                mostRewardingSlot
            );

        }
    }

    // base case khusus ga ada jalur lagi
    slot.filledSlot = currentSlotIdx;
    int currentTotalReward = slot.calculateReward(sequence, sequenceLength);
    if(currentTotalReward > *maxReward)
    {
        mostRewardingSlot->CopyFrom(slot);
        *maxReward = currentTotalReward;
    }

}

/// @brief Get the result packed inside SolveData for passing data outside dll
/// @param bufferSize 
/// @param width width of matrix
/// @param height height of matrix
/// @param matrix token matrix that can be marken
/// @param sequenceLength length of sequence 
/// @param sequence 
/// @return 
CrackData getOptimalSolution(int bufferSize, int width, int height, MarkableToken** matrix, int sequenceLength, Sequence sequence[])
{
    
    clock_t startTime = clock();

    TokenSlot mostRewardingSlot(bufferSize);
    TokenSlot slot(bufferSize);
    int maxReward = INT_MIN;

    // Start from horizontal
    recursion(
        matrix, width, height,
        slot, 0,
        true,
        &maxReward,
        sequence, sequenceLength,
        0, 0,
        &mostRewardingSlot
    );

    // Output
    CrackData solveData = {mostRewardingSlot, maxReward, clock() - startTime};
    return solveData;
}