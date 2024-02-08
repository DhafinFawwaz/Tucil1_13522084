#include "sequence.h"

void Sequence::Debug()
{
    cout << "[ ";
    for(int i = 0; i < count; i++)
    {
        cout << buffer[i] << " ";
    }
    cout << "]" << " +" << reward << endl;
}