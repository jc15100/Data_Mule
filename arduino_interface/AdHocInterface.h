#include <string.h>
#include <fstream>

class Session{
	public:
        std::string id;

        Session(): isOpen(false) {}
        ~Session();
	
        void open(std::string sensorname);
        void write(float data);

        //add more later
        void close();
        void send();

	private:
        bool isOpen;
        std::ofstream file;
};

