#include "sequence.h"

Sequence::Sequence()
{
    count = 0;
    reward = 0;
    buffer = new Token[1];
    bufferSize = 2;
}

void Sequence::push_back(Token token)
{
    if(count == bufferSize)
    {
        Token* newBuffer = new Token[bufferSize * 2];
        for(int i = 0; i < bufferSize; i++)
        {
            newBuffer[i] = buffer[i];
        }
        buffer = newBuffer;
        bufferSize *= 2;
        
    }
    buffer[count] = token;
    count++;
}
bool Sequence::isEqual(Sequence sequence)
{
    if(count != sequence.count)
    {
        return false;
    }
    for(int i = 0; i < count; i++)
    {
        if(buffer[i] != sequence.buffer[i])
        {
            return false;
        }
    }
    return true;
}
void Sequence::print()
{
    cout << "[ ";
    for(int i = 0; i < count; i++)
    {
        cout << buffer[i] << " ";
    }
    cout << "]" << " +" << reward << endl;
}