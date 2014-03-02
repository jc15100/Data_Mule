#include "AdHocInterface.h"
#include <sys/time.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <sstream>
#include <iterator>

using namespace std;

Session::Session(){
    isOpen = false;
    data_directory = "/home/root/mule_data/";
    // check data directory exists, otherwise create it
    struct stat dir_stat;
    
    if(stat(data_directory.c_str(), &dir_stat) != 0){
        mkdir(data_directory.c_str(), S_IRWXU);
    }
}

Session::~Session(){}

/* function open(string, string): creates a unique file to store data of
 * <sensorname> and carries data of type <typeofdata> (eg Celcius, pressure, etc) */
void Session::open(string sensorname, string typeofdata){
    timeval current;
    gettimeofday(&current, 0);

    stringstream filename;
    filename << data_directory << sensorname << (current.tv_sec + current.tv_usec*10e6);
    filename >> sessionid;

    // open data file and write header
    file.open(sessionid.c_str(), std::ofstream::out | std::ofstream::app);
    file << sensorname << endl;
	file << typeofdata << endl;

    isOpen = true;
}

/* function write(float): writes a single datapoint (float) to file*/
void Session::write(float data){
    file << data << endl;
}

/* function write(vector): writes an array of datapoints(floats) to file*/
void Session::write(vector<float> data){
    ostream_iterator<float> data_it(file, "\n");
    copy(data.begin(), data.end(), data_it);
}

/* function close(): closes the file to write, puts the data on the ad-hoc network */
void Session::close(){
    file.close();
    isOpen = false;

    /* put data on the ad-hoc network */
    this->send();
}

/* passes on the file to our python backend */
void Session::send(){
    stringstream comm;
    comm << "python /home/root/mule/cpp_bridge.py " << data_directory << "mule_data.cmdb" << "sessionid";
    int res = system(comm.str().c_str());
    if(res){
        printf("Error saving to ad-hoc network!\n");
    }
}

int main(){
    Session test;

    //test writing single value
    test.open("temperature", "Celcius");
    test.write(4.56);
    test.close();

    //test writing data stream
    test.open("camera", "pixel");
    vector<float> data;
    data.push_back(4.5);
    data.push_back(3.5);
    data.push_back(2.5);
    data.push_back(1.5);
    test.write(data);
    test.close();

    return 0;
}
