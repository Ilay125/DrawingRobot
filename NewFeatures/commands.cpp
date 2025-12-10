#include "commands.h"
#include <cmath>

Move::Move(double x0, double y0) {
    this->x0 = x0;
    this->y0 = y0;
}

int Move::draw() {
    // pen is up so it can move in whatever curve

    // lift up
    // move(x0, y0)
    // pull down

    return 0;
}

Line::Line(double x0, double y0, double x1, double y1) {
    this->x0 = x0;
    this->y0 = y0;
    this->x1 = x1;
    this->y1 = y1;
}

int Line::draw() {
    double slope = (this->y1 - this->y0) / (this->x1 - this->x0);
    // y = y0 + m (x-x0) I know my linear algebra

    // lambda function that generate y for given x
    auto y = [this, slope](double x) {
        return this->y0 + slope * (x - this->x0);
    };

    double dist = sqrt((this->x1 - this->x0)*(this->x1 - this->x0) +
                       (this->y1 - this->y0)*(this->y1 - this->y0));
    
    int steps = static_cast<int>(dist / MICROSTEP);

    double x_start = this->x0;

    for (int s = 0; s < steps; s++) {
        double x_end = x_start + MICROSTEP;

        if (x_end > this->x1) {
            x_end = this->x1;  // clamp to endpoint
        }

        double y_start = y(x_start);
        double y_end = y(x_end);

        // move from (x_start, y_start) -> (x_end, y_end)

        x_start = x_end;  // prepare for next step
    }

    // final move to exact endpoint in case we didn't land exactly
    double y_final = y(this->x1);
    // move(x_start, y(x_start)) -> (x1, y_final);

    return 0;
}

Cubic::Cubic(double x0, double y0, double x1, double y1,
             double x2, double y2, double x3, double y3) {
    this->x0 = x0;
    this->y0 = y0;
    this->x1 = x1;
    this->y1 = y1;
    this->x2 = x2;
    this->y2 = y2;
}

int Cubic::draw() {
    // cubic Bézier lambda: returns (x, y) via reference parameters
    auto bezier = [this](double t, double &x, double &y) {
        double u = 1.0 - t;
        x = u*u*u*this->x0 + 3*u*u*t*this->x1 + 3*u*t*t*this->x2 + t*t*t*this->x3;
        y = u*u*u*this->y0 + 3*u*u*t*this->y1 + 3*u*t*t*this->y2 + t*t*t*this->y3;
    };

    double t = 0.0;
    double x_prev, y_prev;
    bezier(t, x_prev, y_prev);

    while (t < 1.0) {
        double t_next = t + 0.001;  // start small
        if (t_next > 1.0) t_next = 1.0;

        double x_next, y_next;
        bezier(t_next, x_next, y_next);

        // increase t_next until the distance >= MICROSTEP
        while (std::sqrt((x_next - x_prev)*(x_next - x_prev) +
                         (y_next - y_prev)*(y_next - y_prev)) < MICROSTEP && t_next < 1.0) {
            t_next += 0.001;
            if (t_next > 1.0) t_next = 1.0;
            bezier(t_next, x_next, y_next);
        }

        // move from previous point -> next point
        // move(x_prev, y_prev) -> (x_next, y_next)

        t = t_next;
        x_prev = x_next;
        y_prev = y_next;
    }

    // final move to exact endpoint
    double x_final = this->x3;
    double y_final = this->y3;
    // move(x_prev, y_prev) -> (x_final, y_final);

    return 0;
}