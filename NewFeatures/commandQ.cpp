#include "commandQ.h"

CommandQueue::CommandQueue() {
    this->size = 0;
}

void CommandQueue::add_command(Command* c) {
    this->queue.push(c);
    this->size++;
}

void CommandQueue::draw() {
    while (!this->queue.empty()) {
        Command* c = queue.front();
        queue.pop();
        c->draw();
        delete c;
    }
}

void CommandQueue::parse(unsigned char data[], int size) {
    int idx = 0;
    double start_x = 0;
    double start_y = 0;
    double curr_x = 0;
    double curr_y = 0;

    while (idx < size) {
        Command* c = nullptr;

        switch(data[idx]) {
            case 'M': {
                start_x = data[idx + 1] / 10.0;
                start_y = data[idx + 2] / 10.0;

                curr_x = start_x;
                curr_y = start_y;

                c = new Move(start_x, start_y);

                idx += 3;
                break;
            }

            case 'L': {
                double x1 = data[idx + 1] / 10.0;
                double y1 = data[idx + 2] / 10.0;

                c = new Line(curr_x, curr_y, x1, y1);

                curr_x = x1;
                curr_y = y1;

                idx += 3;
                break;
            }

            case 'C': {
                double x1 = data[idx + 1] / 10.0;
                double y1 = data[idx + 2] / 10.0;
                double x2 = data[idx + 3] / 10.0;
                double y2 = data[idx + 4] / 10.0;
                double x3 = data[idx + 5] / 10.0;
                double y3 = data[idx + 6] / 10.0;

                c = new Cubic(curr_x, curr_y, x1, y1, x2, y2, x3, y3);

                curr_x = x3;
                curr_y = y3;

                idx += 7;
                break;
            }
            case 'Z': {
                c = new Line(curr_x, curr_y, start_x, start_y);

                idx += 1;
                break;
            }

            default:
                //printf("Unknown command: %c at index %d\n", data[idx], idx);
                return; 

        }

        if (c) {
            this->add_command(c);
        }
          
    }

}