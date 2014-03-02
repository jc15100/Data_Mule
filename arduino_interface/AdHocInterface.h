#ifndef AdHocInterface_h
#define AdHocInterface_h

#include <string.h>
#include <fstream>
#include <vector>

class Session{
	public:
        Session();
        ~Session();

        /* function open(string, int): opens a session given a sensor name and size of data to be recorded */
        void open(std::string sensorname, int size);

        /* function writes a single float datapoint to file*/
        void write(float data);

        /* function writes a stream of float datapoints to file*/
        void write(std::vector<float> data);

        /* function close(): closes a data session and puts the data on the ad-hoc network*/
        void close();

	private:
        void send();

        bool isOpen;
        std::ofstream file;
        std::string sessionid;
        std::string data_directory;
};

#endif

