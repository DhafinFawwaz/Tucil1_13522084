
#ifndef SEQUENCE_H
#define SEQUENCE_H

#include "token.h"

struct Sequence{
    int count;
    int reward;
    vector<Token> buffer;
    void Debug();
};
#endif

