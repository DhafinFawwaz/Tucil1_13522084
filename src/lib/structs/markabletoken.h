#ifndef MARKABLETOKEN_H
#define MARKABLETOKEN_H

#include "token.h"

struct MarkableToken{
    Token token;
    bool isMarked;
};

#endif