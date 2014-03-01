#include <string>
#include <fstream>

class Session{
	public:
	std::string id;
	
	Session() {isOpen(false)}
	~Session();
	
	void open(std::string id, int size);
	void write(float data);
	
	//add more later
	void close();
	void send();

	private:
	bool isOpen;
	FILE* file;
};

