#include "AdHocInterface.h"
#include <sys/time.h>
#include <sstream>

using namespace std;

void Session::open(string sensorname){
    timeval current;
    gettimeofday(&current, 0);

    stringstream filename;
    string datafile;
    filename << sensorname << (current.tv_sec + current.tv_usec*10e6);
    filename >> datafile;

    file.open(filename.str().c_str(), std::ofstream::out | std::ofstream::app);
    isOpen = true;
}

Session::~Session(){}

void Session::write(float data){
    file << data << endl;
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
    test.open("temperature");
    test.write(4.56);
    test.close();
    return 0;
}



