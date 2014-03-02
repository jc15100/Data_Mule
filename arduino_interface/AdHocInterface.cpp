//#include "Arduino.h"
#include "AdHocInterface.h"
#include <sys/time.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <sstream>
#include <iterator>

using namespace std;

Session::Session(){
    isOpen = false;
    data_directory = "/tmp/node_data/";
    // check data directory exists, otherwise create it
    struct stat dir_stat;
    if(stat(data_directory.c_str(), &dir_stat) != 0){
        mkdir(data_directory.c_str(), S_IRWXU);
    }
}

Session::~Session(){}

/* function open(string, int): creates a data file given specified number of points */
void Session::open(string sensorname, int size){
    timeval current;
    gettimeofday(&current, 0);

    stringstream filename;
    filename << data_directory << sensorname << (current.tv_sec + current.tv_usec*10e6);
    filename >> sessionid;

    // open data file and write header
    file.open(sessionid.c_str(), std::ofstream::out | std::ofstream::app);
    file << sensorname << endl;
    file << sizeof(float)*size << endl;

    isOpen = true;
}

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

    /* put data on the ad-hoc network */
    this->send();
}

void Session::send(){
    stringstream comm;
    comm << "python cpp_bridge.py " << sessionid;
    int res = system(comm.str().c_str());
    printf("%d \n", res);
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



