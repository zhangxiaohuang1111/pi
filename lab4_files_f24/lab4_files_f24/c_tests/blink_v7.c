//
//  jfs9, 10/18/16  v2, add variable for altering frequency
//                  v3 add internal timer
//                  v4 delayMicroseconds and Pinvalue for better behavior...
//        3/24/17   v6 nanosleep....
//        10/24/2020 v7 convert from wiring pi to pigpio
//        4/2/2021   check
//        10/10/2021 check
//        3/28/2022  check
//        10/24/2024 modify to accept frequency input

#include <stdlib.h>
#include <stdio.h>
#include <pigpio.h>
#include <time.h>

#define NSEC_PER_SEC  1000000000 /* The number of nsecs per sec. */

struct timespec t;

int main (int argc, char** argv)
{
  int period;  // half-period for delay in nsec
  int PinValue = 0;  // hi/low indication of output Pin
  unsigned int current_sec, start_sec;
  float freq;
  
  if (argc >= 2 && atof(argv[1]) > 0) {  // if we have a positive frequency input
    freq = atof(argv[1]);
    period = (int)(NSEC_PER_SEC / (2 * freq));  // calculate half-period in nsec
  } else {
    printf("Usage: %s <frequency_in_Hz>\n", argv[0]);
    return -1;
  }
  
  printf("Set frequency to %f Hz\n", freq);
  printf("Set 1/2 period to %d nanoseconds\n", period);

  gpioInitialise();

  clock_gettime(CLOCK_MONOTONIC, &t); // setup timer t
  t.tv_nsec += period;   // add in initial period
  start_sec = t.tv_sec;
  current_sec = 0;

  gpioSetMode(16, PI_OUTPUT);  // set GPIO 16 to output

  while (current_sec < 100) {   // run the loop for 100 sec
    gpioWrite(16, PinValue);  // Send signal on pin 16
    clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &t, NULL); // delay a bit...
    PinValue = PinValue ^ 1;  // Flip the value of the output pin
    t.tv_nsec += period;   // add in half-period

    while (t.tv_nsec >= NSEC_PER_SEC) {   // This accounts for 1 sec rollover
      t.tv_nsec -= NSEC_PER_SEC;
      t.tv_sec++;
      current_sec = t.tv_sec - start_sec;  // how many seconds since we started?
    }
  }
  printf("Stopped at %d seconds\n", current_sec);
  gpioTerminate();  // exit piGPIO
  return 0;
}