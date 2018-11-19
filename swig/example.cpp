/*
 * =====================================================================================
 *       Copyright (c), 2013-2020, xxx.
 *       Filename:  example.cpp
 *
 *    Description:  1. swig -c++ -python example.i
 *         Others:  2. python setup.py build_ext --inplace
 *                  3. python 
 *                  4. import example 
 *                  5. example.Example().SayHello()
 *
 *        Version:  1.0
 *        Created:  11/19/2018 11:44:19 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Joy. Hou (hwt), 544088192@qq.com
 *   Organization:  xxx
 *
 * =====================================================================================
 */

#include "example.h"
using namespace std;

void Example::SayHello()
{
    cout<<"hello"<<endl;
}
vector<string> Example::GetName()
{
    vector<string> a = vector<string>();
    return a;
}
