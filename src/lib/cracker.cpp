#include "cracker.h"
using namespace std;


/*
void debug(MarkableToken** matrix, int width, int height)
{
    for(int i = 0; i < height; i++)
    {
        cout << "[ ";
        for(int j = 0; j < width; j++)
        {
            if(matrix[i][j].isMarked) cout << "\033[0;32m" << matrix[i][j].token << "\033[0;37m ";
            else cout << matrix[i][j].token << " ";
        }
        cout << "]" << endl;
    }
}

void debugMatrixSlot(MarkableToken** matrix, int width, int height, TokenSlot slot)
{
    for(int i = 0; i < height; i++)
    {
        cout << "[ ";
        for(int j = 0; j < width; j++)
        {
            bool isFound = false;
            for(int k = 0; k < slot.bufferSize; k++)
            {
                if(slot.slotList[k].x == j && slot.slotList[k].y == i)
                {
                    cout << "\033[0;32m" << matrix[i][j].token << "\033[0;37m ";
                    isFound = true;
                    break;
                }
            }
            if(!isFound) cout << matrix[i][j].token << " ";
        }
        cout << "]" << endl;
    }
}
*/
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
        int currentTotalReward = slot.calculateReward(sequence, sequenceLength);
        if(currentTotalReward > *maxReward)
        {
            mostRewardingSlot->CopyFrom(slot);
            *maxReward = currentTotalReward;
        }

        // Debug
        // cout << "======== base ========" << endl;
        // debug(matrix, width, height);
        // cout << "curr: " << currentTotalReward << endl;
        // slot.Debug();
        // cout << "max: " << *maxReward << endl;
        // (*mostRewardingSlot).Debug();
        // for(int i = 0; i < sequenceLength; i++)
        // {
        //     sequence[i].Debug();
        // }
        // string temp;
        // cin >> temp;
        // cout << "==============" << endl;        
        
        return;
    }

    // isHorizontal udah direverse pas fungsi rekursinya dipanggil
    if(isHorizontal)
    {
        for(int j = 0; j < width; j++)
        {
            if(matrix[posY][j].isMarked) continue;

            // everytime a new mark is set, the previous needs to be unset. Like swapping
            // happens when backtracking. indexHasBeenFilled just to make sure the value is initialized
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
    int currentTotalReward = slot.calculateReward(sequence, sequenceLength);
    if(currentTotalReward > *maxReward)
    {
        mostRewardingSlot->CopyFrom(slot);
        *maxReward = currentTotalReward;
    }

    // Debug
    // cout << "======== end ========" << endl;
    // debug(matrix, width, height);
    // cout << "curr: " << currentTotalReward << endl;
    // slot.Debug();
    // cout << "max: " << *maxReward << endl;
    // (*mostRewardingSlot).Debug();
    // for(int i = 0; i < sequenceLength; i++)
    // {
    //     sequence[i].Debug();
    // }
    // string temp;
    // cin >> temp;
    // cout << "==============" << endl;
    
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
    // Start Debug
    // cout << "Buffer size: " << bufferSize << endl;
    // cout << "Width: " << width << endl;
    // cout << "Height: " << height << endl;
    // cout << "Matrix: " << endl;
    // for(int i = 0; i < height; i++)
    // {
    //     for(int j = 0; j < width; j++)
    //     {
    //         cout << matrix[i][j].token << " ";
    //     }
    //     cout << endl;
    // }
    // cout << "Sequence length: " << sequenceLength << endl;
    // cout << "Sequence: " << endl;
    // for(int i = 0; i < sequenceLength; i++)
    // {
    //     int length = sequence[i].bufferSize;
    //     for(int j = 0; j < length; j++)
    //     {
    //         cout << sequence[i].buffer[j] << " ";
    //     }
    //     cout << endl;
    //     cout << sequence[i].reward << endl;
    // }
    // cout << endl;
    // End Debug

    clock_t startTime = clock();

    TokenSlot mostRewardingSlot(bufferSize);
    TokenSlot slot(bufferSize);
    int maxReward = -1;

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

    // Debug
    // debugMatrixSlot(matrix, width, height, mostRewardingSlot);
    // mostRewardingSlot.Debug();

    // Output
    CrackData solveData = {mostRewardingSlot, maxReward, clock() - startTime};
    return solveData;
}
int test()
{
    return 43;
}