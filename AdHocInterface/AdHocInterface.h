#ifndef AdHocInterface_h
#define AdHocInterface_h

//#include "Arduino.h"
#include <string.h>
#include <fstream>
#include <vector>

class Session{
	public:
        Session();
        ~Session();

		/* opens a session to record information to pass onto the network
		 * sensorname: name of sensor (eg temperature, wind speed)
		 * typeofdata: type of data collected (eg Celcius, MPH) */
        void open(std::string sensorname, std::string typeofdata);

		/* add a data point to the session
		 * data: the datapoint to add (eg 12, 32.9) */
        void write(float data);

		/* add multiple data points to the session
		 * data: a vector of datapoints to add (eg {1, 2, 3, 4}) */
        void write(std::vector<float> data);

		/* close the session and put the collected data on the ad-hoc network
		 * to eventually be uploaded to the cloud */
        void close();

	private:
        void send();

        bool isOpen;
        std::ofstream file;
        std::string sessionid;
        std::string data_directory;
};

#endif

