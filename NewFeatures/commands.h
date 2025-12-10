#ifndef __COMMANDS__
#define __COMMANDS__

#define MICROSTEP 0.1 // MOVE TO CONFIG

class Command {
    public:
        virtual int draw() = 0;
        virtual void print_command() = 0;
        virtual ~Command() = default;
};

class Move: public Command {
    double x0;
    double y0;

    public:
        Move(double x0, double y0);
        int draw();
        void print_command();
};

class Line: public Command {
    double x0;
    double y0;
    double x1;
    double y1;

    public:
        Line(double x0, double y0, double x1, double y1);
        int draw();
        void print_command();
};

class Cubic: public Command {
    double x0;
    double y0;
    double x1;
    double y1;
    double x2;
    double y2;
    double x3;
    double y3;

    public:
        Cubic(double x0, double y0, double x1, double y1,
             double x2, double y2, double x3, double y3);
        int draw();
        void print_command();
};

#endif