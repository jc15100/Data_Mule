#ifndef AdHocInterface_h
#define AdHocInterface_h

#include <string.h>
#include <fstream>
#include <vector>

class Session{
	public:
        Session();
        ~Session();

        /* function open(string, int): creates a data file given specified number of points */
        void open(std::string sensorname, int size);

        /* function writes a single float datapoint to file*/
        void write(float data);

        /* function writes a stream of float datapoints to file*/
        void write(std::vector<float> data);

        void close();
        void send();

	private:
        bool isOpen;
        std::ofstream file;
        std::string sessionid;
        std::string data_directory;
};

#endif

