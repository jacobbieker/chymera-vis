//
// Created by jacob on 5/3/16.
//

#include "binaryReader.h"
#include <fstream>
#include <vector>
#include <string>

using namespace std;

struct Point
{
    double x, y, z;
};

const int RECORD_DELIMITER_LENGTH = 4;

bool ReadPoints(const string& fileName, vector& points)
{
    int nbPoints;

    // clear the points
    points.clear();

    // open file in binary mode
    ifstream input(fileName.c_str(), ios::binary);

    if (input.good())
    {
        // read number of points
        input.seekg(RECORD_DELIMITER_LENGTH, ios::cur);
        input.read((char*) &nbPoints, sizeof(nbPoints));
        input.seekg(RECORD_DELIMITER_LENGTH, ios::cur);

        // set vector size
        points.resize(nbPoints);

        // read each point
        for (int i = 0; i < nbPoints; ++i)
        {
            input.seekg(RECORD_DELIMITER_LENGTH, ios::cur);

            input.read((char*) &points[i].x, sizeof(points[i].x));
            input.read((char*) &points[i].y, sizeof(points[i].y));
            input.read((char*) &points[i].z, sizeof(points[i].z));

            input.seekg(RECORD_DELIMITER_LENGTH, ios::cur);
        }

        return true;
    }
    else
    {
        return false;
    }
}

int main() {
    string filename = "saved.005000";

}