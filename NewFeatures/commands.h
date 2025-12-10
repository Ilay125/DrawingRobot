#ifndef __COMMANDS__
#define __COMMANDS__

class Command {
    public:
        virtual int draw(int steps=100) = 0;
        virtual ~Command() = default;
};

class Move: public Command {
    double x0;
    double y0;

    public:
        Move(double x0, double y0);
        int draw(int steps);
};

class Line: public Command {
    double x0;
    double y0;
    double x1;
    double y1;

    public:
        Line(double x0, double y0, double x1, double y1);
        int draw(int steps);
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
        int draw(int steps);
};

#endif