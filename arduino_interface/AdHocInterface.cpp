//#include "Arduino.h"
#include "AdHocInterface.h"
#include <sys/time.h>
#include <sstream>
#include <iterator>

using namespace std;

/* function open(string, int): creates a data file given specified number of points */
void Session::open(string sensorname, int size){
    timeval current;
    gettimeofday(&current, 0);

    stringstream filename;
    string datafile;
    filename << sensorname << (current.tv_sec + current.tv_usec*10e6);
    filename >> datafile;

    // open data file and write header
    file.open(filename.str().c_str(), std::ofstream::out | std::ofstream::app);
    file << sensorname << endl;
    file << sizeof(float)*size << endl;

    isOpen = true;
}

Session::~Session(){}

/* function write(float): writes a single float datapoint to file*/
void Session::write(float data){
    file << data << endl;
}

/* function write(vector): writes a stream of float datapoints to file*/
void Session::write(vector<float> data){
    ostream_iterator<float> data_it(file, "\n");
    copy(data.begin(), data.end(), data_it);
}

void Session::close(){
    file.close();
    isOpen = false;
}

void Session::send(){
    // call Andrew's comm API
}

int main(){
    Session test;

    //test writing single value
    test.open("temperature", 1);
    test.write(4.56);
    test.close();

    //test writing data stream
    test.open("camera", 4);
    vector<float> data;
    data.push_back(4.5);
    data.push_back(3.5);
    data.push_back(2.5);
    data.push_back(1.5);
    test.write(data);
    test.close();
    return 0;
}



