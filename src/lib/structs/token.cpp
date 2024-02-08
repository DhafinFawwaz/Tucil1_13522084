#include "token.h"

Token Token::operator=(char c[2])
{
    value[0] = c[0];
    value[1] = c[1];
    return *this;
}
bool Token::operator==(Token t)
{
    return value[0] == t.value[0] && value[1] == t.value[1];
}
bool Token::operator!=(Token t)
{
    return !(value[0] == t.value[0] && value[1] == t.value[1]);
}
/// @brief For printing the t.value cutting the trailing \0
/// @param os 
/// @param t 
/// @return 
ostream& operator<<(ostream& os, const Token& t) {
    os << t.value[0] << t.value[1];
    return os;
}