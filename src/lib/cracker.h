#ifndef CRACKER_H
#define CRACKER_H

#include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <time.h>
#include <stdio.h>
#include <chrono>
#include "structs/token.h"
#include "structs/sequence.h"
#include "structs/tokenslot.h"
#include "structs/markabletoken.h"
#include "structs/crackdata.h"
using namespace std;

void debug(MarkableToken** matrix, int width, int height);
void debugMatrixSlot(MarkableToken** matrix, int width, int height, TokenSlot slot);

void recursion(
    MarkableToken** matrix, int width, int height, 
    TokenSlot slot, int currentSlotIdx, 
    bool isHorizontal, 
    int* maxReward, 
    Sequence sequence[], int sequenceLength, 
    int posX, int posY,
    TokenSlot* mostRewardingSlot);

/// @brief Get the result packed inside SolveData for passing data outside dll
/// @param bufferSize 
/// @param width width of matrix
/// @param height height of matrix
/// @param matrix token matrix that can be marken
/// @param sequenceLength length of sequence 
/// @param sequence 
/// @return 


extern "C" {
    CrackData getOptimalSolution(int bufferSize, int width, int height, MarkableToken** matrix, int sequenceLength, Sequence sequence[]);
    int test();
}

#endif