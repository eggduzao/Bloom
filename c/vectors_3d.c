#include <stdio.h>
#ifdef __arm__
#define LIBQUAT_ARM
#include <arm_math.h>
#else
#include <math.h>
#endif
#include <assert.h>

#include "geometry_datatypes.h"

vec_3d vector_sub(const vec_3d *a, const vec_3d *b)
{
    vec_3d out;
#ifdef LIBQUAT_ARM
    arm_sub_f32((float *)a, (float *)b, (float *)&out);
#else
    out.x = a->x - b->x;
    out.y = a->y - b->y;
    out.z = a->z - b->z;
#endif

    return out;
}

vec_3d vector_add(const vec_3d *a, const vec_3d *b)
{
    vec_3d out;
#ifdef LIBQUAT_ARM
    arm_add_f32((float *)a, (float *)b, (float *)&out);
#else
    out.x = a->x + b->x;
    out.y = a->y + b->y;
    out.z = a->z + b->z;
#endif

    return out;
}

float dot_prod(const vec_3d *a, const vec_3d *b)
{
    float dot;
#ifdef LIBQUAT_ARM
    arm_dot_prod_f32((float *)a, (float *)b, &dot);
#else
    dot = a->x * b->x;
    dot += a->y * b->y;
    dot += a->z * b->z;
#endif

    return dot;
}

vec_3d vector_prod(const vec_3d *a, const vec_3d *b)
{
    vec_3d out;
    out.x = a->y * b->z - a->z * b->y;
    out.y = -a->x * b->z + a->z * b->x;
    out.z = a->x * b->y - a->y * b->x;

    return out;
}

const char *print_vector(const vec_3d *a, const char *name)
{
    static char vec_str[100];
    snprintf(vec_str, 99, "vec(%s) = (%.3g)i + (%.3g)j + (%.3g)k\n", name, a->x,
             a->y, a->z);
    return vec_str;
}

float vector_norm(const vec_3d *a)
{
    float n = dot_prod(a, a);
#ifdef LIBQUAT_ARM
    arm_sqrt_f32(*n, n);
#else
    n = sqrtf(n);
#endif

    return n;
}

vec_3d unit_vec(const vec_3d *a)
{
    vec_3d n = {0};

    float norm = vector_norm(a);
    if (fabsf(norm) < EPSILON)
    {
        return n;
    }

    if (norm != 1.F)
    {
        n.x = a->x / norm;
        n.y = a->y / norm;
        n.z = a->z / norm;
    }
    return n;
}

mat_3x3 get_cross_matrix(const vec_3d *a)
{
    mat_3x3 A = {0., -a->z, a->y, a->z, 0., -a->x, -a->y, a->x, 0.};
    return A;
}

