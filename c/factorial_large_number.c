#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct _large_num
{
    char *digits;
    unsigned int num_digits;
} large_num;


large_num *new_number(void)
{
    large_num *new_num = (large_num *)malloc(sizeof(large_num));
    new_num->num_digits = 1;
    new_num->digits = (char *)malloc(1 * sizeof(char));
    new_num->digits[0] = 1;
    return new_num;
}


void delete_number(large_num *num)
{
    free(num->digits);
    free(num);
}


void add_digit(large_num *num, unsigned int value)
{
    if (value > 9)
    {
        fprintf(stderr, "digit > 9!!\n");
        delete_number(num);
        exit(EXIT_FAILURE);
    }

    num->num_digits++;
    num->digits = (char *)realloc(num->digits, num->num_digits * sizeof(char));
    num->digits[num->num_digits - 1] = value;
}


void multiply(large_num *num, unsigned long n)
{
    int i;
    unsigned long carry = 0, temp;
    for (i = 0; i < num->num_digits; i++)
    {
        temp = num->digits[i] * n;
        temp += carry;
        if (temp < 10)
            carry = 0;
        else
        {
            carry = temp / 10;
            temp = temp % 10;
        }
        num->digits[i] = temp;
    }

    while (carry != 0)
    {
        add_digit(num, carry % 10);
        carry /= 10;
    }
}

