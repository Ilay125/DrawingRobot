#ifndef __COMMANDQ__
#define __COMMANDQ__

#include <queue>
#include "commands.h"

class CommandQueue {
    std::queue<Command*> queue;
    int size;

    public:
        CommandQueue();
        void add_command(Command* c);
        void parse(unsigned char data[], int size); // replace char with uint8_t
        void draw();

};

#endif