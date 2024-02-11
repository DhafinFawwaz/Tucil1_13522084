#include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <time.h>
#include <stdio.h>
#include <cstdlib>
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
        Token t = {line[0], line[1]};
        sequence[i].push_back(t);
        int lineLength = line.length();
        int j = 3;
        while(j < lineLength)
        {
            Token t = {line[j], line[j+1]};
            sequence[i].push_back(t);
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
        Token t = {line[0], line[1]};
        sequence[i].push_back(t);
        int lineLength = line.length();
        int j = 3;
        while(j < lineLength)
        {
            Token t = {line[j], line[j+1]};
            sequence[i].push_back(t);
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

#define amountOfUniqueTokensStr "Amount of Unique Tokens: "
#define possibleTokensStr "Possible Tokens: "
#define bufferSizeStr "Buffer Size: "
#define matrixDimensionStr "Matrix Dimension (width height): "
#define sequenceAmountStr "Amount of Sequence: "
#define maximalSequenceLengthStr "Maximal Sequence Length: "
#define generatedMatrixStr "Generated Matrix: "

int randomRange(int min, int max)
{
    return rand() % (max - min + 1) + min;
}

bool isSequenceExistInListOfSequence(Sequence sequence, Sequence* sequenceList, int sequenceListLength)
{
    for(int i = 0; i < sequenceListLength; i++)
    {
        if(!sequence.isEqual(sequenceList[i]))
        {
            return false;
        }
    }
    return true;
}

void startByAutoGenerateInput()
{
    // jumlah_token_unik
    cout << amountOfUniqueTokensStr << endl;
    int uniqueTokenCount;
    cin >> uniqueTokenCount;
    
    // token
    cout << possibleTokensStr << endl;
    Token possibleTokens[uniqueTokenCount];
    for(int i = 0; i < uniqueTokenCount; i++)
    {
        char c[2];
        cin >> c;
        possibleTokens[i] = {c[0], c[1]};
    }

    // ukuran_buffer
    cout << bufferSizeStr;
    int bufferSize;
    cin >> bufferSize;

    // ukuran_matriks
    cout << matrixDimensionStr << endl;
    int width, height;
    cin >> width >> height;

    // jumlah_sekuens
    cout << sequenceAmountStr;
    int sequenceAmount;
    cin >> sequenceAmount;

    // ukuran_maksimal_sekuens
    cout << maximalSequenceLengthStr;
    int maxSequenceLength;
    int minSequenceLength = 2;
    cin >> maxSequenceLength;

    // generate matrix
    MarkableToken** matrix;
    matrix = new MarkableToken*[height];

    // seed random
    srand(time(NULL));

    // generate matrix
    cout << generatedMatrixStr << endl;
    for(int i = 0; i < height; i++)
    {
        matrix[i] = new MarkableToken[width];
        for(int j = 0; j < width; j++)
        {
            int randomIndex = rand() % uniqueTokenCount;
            matrix[i][j].token = possibleTokens[randomIndex];
            matrix[i][j].isMarked = false;

            cout << matrix[i][j].token << ' ';
        }
        cout << endl;
    }

    // generate sequence
    Sequence sequence[sequenceAmount];
    int i = 0;
    while(i < sequenceAmount)
    {
        int sequenceLength = randomRange(minSequenceLength, maxSequenceLength);
        for(int j = 0; j < sequenceLength; j++)
        {
            int randomIndex = rand() % uniqueTokenCount;
            sequence[i].push_back(possibleTokens[randomIndex]);
        }
        // unique check
        if(isSequenceExistInListOfSequence(sequence[i], sequence, sequenceLength))
        {
            continue;
        }

        cout << "Sequence" << i << ':' << endl;
        for(int j = 0; j < sequenceLength; j++)
        {
            cout << sequence[i].buffer[j] << ' ';
        }
        cout << endl;
        // range reward 10 - 50
        int reward = randomRange(10, 50);
        sequence[i].reward = reward;
        cout << "reward: " << reward << endl;
        i++;
    }        

    CrackData data = getOptimalSolution(bufferSize, width, height, matrix, sequenceAmount, sequence);
    printSolveData(data);
    askForSavingOutput(data);
}


#define titleStr "Cyberpunk 2077 Breach Protocol Cracker"
#define chooseOptionStr "Choose option (number): "
#define option1Str "1. Input by typing manually"
#define option2Str "2. Input from file"
#define option3Str "3. Auto generate input"
#define option4Str "4. Exit"

void cliScreen()
{
    cout << titleStr << endl << endl;
    cout << option1Str << endl;
    cout << option2Str << endl;
    cout << option3Str << endl;
    cout << option4Str << endl;
    cout << endl << chooseOptionStr;

    int option = 0;
    while(!(option >= 1 && option <= 3))
    {
        cin >> option;
        if(option == 1) startByTyping();
        else if(option == 2)
        {
            string path;
            cout << "File path: ";
            cin >> path;
            startByPath(path);
        }
        else if(option == 3) startByAutoGenerateInput();
        else if(option == 4) return;
        else if(!cin.good())
        {
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            cout << "Please input a number!: ";
        }
        else cout << "Please choose between range 1 - 3!: ";
    }
}


int main(int argc, char* argv[])
{
    // from file
    if(argc > 1) startByPath(argv[1]);
    else cliScreen();
    return 0;
}