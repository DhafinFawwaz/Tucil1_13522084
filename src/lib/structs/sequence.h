
#ifndef SEQUENCE_H
#define SEQUENCE_H

#include "token.h"

struct Sequence{

    int count;
    int reward;
    Token* buffer; // cant use vector here because of dll
    int bufferSize;
    Sequence();
    void push_back(Token token);
    bool isEqual(Sequence sequence);
    void print();
};
#endif

