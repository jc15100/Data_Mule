#include "AdHocInterface.h"
#include <iostream.h>

void Session::open(std::string id, int size){
	std::stringstream filepath = "~/data_" << id;
	
	file = fopen(filepath, "w+");


}

