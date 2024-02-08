#include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <time.h>
#include <stdio.h>
#include "../lib/cracker.h"
using namespace std;

/// @brief Save data to path
/// @param data 
/// @param path 
void saveToPath(CrackData data, string path)
{
    // same as printSolveData but to file
    ofstream file(path);
    file << data.maxReward << endl;
    for(int i = 0; i < data.mostRewardingSlot.bufferSize; i++)
    {
        file << data.mostRewardingSlot.slotList[i].token << ' ';
    }
    file << endl;
    for(int i = 0; i < data.mostRewardingSlot.bufferSize; i++)
    {
        // plus 1 because it started from 1
        file << data.mostRewardingSlot.slotList[i].x + 1 << ", " << data.mostRewardingSlot.slotList[i].y + 1 << endl;
    }
    file << endl;
    file << data.executionDuration << " ms" << endl;
}

/// @brief ask whether user want to save data to text file or not
/// @param data 
void askForSavingOutput(CrackData data)
{
    cout << endl << "Apakah ingin menyimpan solusi? (y/n)" << endl;
    char c; cin >> c;
    if(c == 'y')
    {
        string savePath;
        cout << "Masukkan path output" << endl;
        cin >> savePath;
        saveToPath(data, savePath);
    }
}

/// @brief Print result
/// @param data 
void printSolveData(CrackData data)
{   
    cout << data.maxReward << endl;
    for(int i = 0; i < data.mostRewardingSlot.bufferSize; i++)
    {
        cout << data.mostRewardingSlot.slotList[i].token << ' ';
    }
    cout << endl;
    for(int i = 0; i < data.mostRewardingSlot.bufferSize; i++)
    {
        // plus 1 because it started from 1
        cout << data.mostRewardingSlot.slotList[i].x + 1 << ", " << data.mostRewardingSlot.slotList[i].y + 1 << endl;
    }
    cout << endl;
    cout << data.executionDuration << " ms" << endl;
}

/// @brief start cli by typing the input manually
void startByTyping()
{
    int bufferSize;
    cin >> bufferSize;

    int width, height;
    cin >> width >> height;

    MarkableToken** matrix;
    matrix = new MarkableToken*[height];
    for(int i = 0; i < height; i++)
    {
        matrix[i] = new MarkableToken[width];
        for(int j = 0; j < width; j++)
        {
            char c[2];
            cin >> c;
            matrix[i][j].token = c;
            matrix[i][j].isMarked = false;
        }
    }

    int sequenceLength;
    cin >> sequenceLength;

    string line;
    Sequence sequence[sequenceLength];
    for(int i = 0; i < sequenceLength; i++)
    {
        cin.ignore();
        getline(cin, line);
        sequence[i].count = 1;
        Token t = {line[0], line[1]};
        sequence[i].buffer.push_back(t);
        int lineLength = line.length();
        int j = 3;
        while(j < lineLength)
        {
            Token t = {line[j], line[j+1]};
            sequence[i].buffer.push_back(t);
            sequence[i].count++;
            j += 3;
        }
        cin >> sequence[i].reward;
    }

    CrackData data = getOptimalSolution(bufferSize, width, height, matrix, sequenceLength, sequence);
    printSolveData(data);
    askForSavingOutput(data);
}

/// @brief start cli by reading the input from file
/// @param path 
void startByPath(string path)
{
    ifstream file(path);
    string line;
    if(!file.is_open())
    {
        cout << "File not found" << endl;
        return;
    }
    getline(file, line);
    int bufferSize = stoi(line);

    getline(file, line);
    int pos = line.find(" ");
    string splitedLine1 = line.substr(0, pos);
    string splitedLine2 = line.substr(pos + 1, line.length());
    int width = stoi(splitedLine1);
    int height = stoi(splitedLine2);


    MarkableToken** matrix;
    matrix = new MarkableToken*[height];
    for(int i = 0; i < height; i++)
    {
        matrix[i] = new MarkableToken[width];
        getline(file, line);
        for(int j = 0; j < width; j++)
        {
            char c[2] = {line[j*3], line[j*3+1]};
            matrix[i][j].token = c;
            matrix[i][j].isMarked = false;
        }
    }

    getline(file, line);
    int sequenceLength = stoi(line);

    Sequence sequence[sequenceLength];
    for(int i = 0; i < sequenceLength; i++)
    {
        getline(file, line);
        sequence[i].count = 1;
        Token t = {line[0], line[1]};
        sequence[i].buffer.push_back(t);
        int lineLength = line.length();
        int j = 3;
        while(j < lineLength)
        {
            Token t = {line[j], line[j+1]};
            sequence[i].buffer.push_back(t);
            sequence[i].count++;
            j += 3;
        }

        getline(file, line);
        sequence[i].reward = stoi(line);
    }

    file.close();

    CrackData data = getOptimalSolution(bufferSize, width, height, matrix, sequenceLength, sequence);
    printSolveData(data);
    askForSavingOutput(data);
}

int main(int argc, char* argv[])
{
    if(argc > 1) startByPath(argv[1]);
    else startByTyping();
    return 0;
}