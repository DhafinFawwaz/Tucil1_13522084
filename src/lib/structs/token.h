#ifndef TOKEN_H
#define TOKEN_H

#include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <time.h>
#include <stdio.h>
using namespace std;

struct Token{
    char value[2];
    Token operator=(char c[2]);
    bool operator==(Token t);
    bool operator!=(Token t);
};

/// @brief For printing the t.value cutting the trailing \0
/// @param os 
/// @param t 
/// @return 
ostream& operator<<(ostream& os, const Token& t);


#endif