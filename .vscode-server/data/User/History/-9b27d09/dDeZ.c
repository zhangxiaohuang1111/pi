//
//  jfs9, 3/17/16   Performance test on C array
//        10/10/17 Check function of code
//        10/24/2020
//        10/10/2021 check
//
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int comp (const void * elem1, const void * elem2)    
{
    int f = *((int*)elem1);
    int s = *((int*)elem2);
    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}

int main()
{
    // Generate data
    const unsigned arraySize = 32768;
    int data[arraySize];

    for (unsigned c = 0; c < arraySize; ++c) {
        data[c] = rand() % 256;
    }

    // 对数组进行排序
    qsort(data, sizeof(data) / sizeof(*data), sizeof(*data), comp);

    printf("size of data = %d, size of *data = %d\n", (int)sizeof(data), (int)sizeof(*data));

    // Start a timer
    clock_t start = clock();  
    long long sum = 0;

    for (unsigned i = 0; i < 20000; ++i)
    {
        // Primary loop
        for (unsigned c = 0; c < arraySize; ++c)
        {
            if (data[c] >= 128)   //  add to sum only if element > 128
                sum += data[c];
        }
    }

    double elapsedTime = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("elapsed time = %3.5f\n", elapsedTime);

    return 0;
}