#include "AdHocInterface.h"
#include <sys/time.h>

using namespace std;

void Session::open(std::string sensorname){
    timeval current;
    gettimeofday(&current, 0);

    std::stringstream filename;
    std::string datafile;
    filename << sensorname << (current.tv_sec + current.tv_usec*10e6);
    filename >> datafile;

    file.open(filename);
    isOpen = true;
}

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



