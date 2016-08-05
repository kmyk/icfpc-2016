#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <boost\rational.hpp>
#include <boost\multiprecision\cpp_int.hpp>
#include <cstdio>
using namespace std;

void solve(int porygon_num,int skelton_num,vector<boost::rational<boost::multiprecision::cpp_int>> vertexes)
{
    cerr << "SOLVE" << endl;
    return;
}

boost::multiprecision::cpp_int stocpp_int(string str)
{
    boost::multiprecision::cpp_int ret = 0;
    for (auto& e : str)
    {
        ret = ret * 10 + e - '0';
    }
    return ret;
}

void get_vertex(vector<boost::rational<boost::multiprecision::cpp_int>>& vertexes)
{
    string vertex;
    cin >> vertex;
    auto stream_vertex = stringstream(vertex);
    boost::rational<boost::multiprecision::cpp_int> r;
    for (int i = 0; i < 2; i++)
    {
        string temp_string;
        getline(stream_vertex, temp_string, ',');
        if (temp_string.find('/') != string::npos)
        {
            string numerator_string;
            string denominator_string;
            auto stream_temp = stringstream(temp_string);
            getline(stream_temp, numerator_string, '/');
            getline(stream_temp, denominator_string, '/');
            r = boost::rational<boost::multiprecision::cpp_int>(stocpp_int(numerator_string), stocpp_int(denominator_string));
        }
        else
        {
            r = boost::rational<boost::multiprecision::cpp_int>(stocpp_int(temp_string), 1);
        }
        vertexes.push_back(r);
        cerr << r << endl;
    }
}

int main(void)
{
    int porygon_num;
    cin >> porygon_num;
    vector<boost::rational<boost::multiprecision::cpp_int>> vertexes;
    for (int num_of_porygon = 0; num_of_porygon < porygon_num; num_of_porygon++)
    {
        int vertex_num;
        cin >> vertex_num;
        for (int num_of_vertex = 0; num_of_vertex < vertex_num; num_of_vertex++)
        {
            get_vertex(vertexes);
        }
    }
    int skelton_num;
    cin >> skelton_num;
    for (int num_of_skelton = 0; num_of_skelton < skelton_num; num_of_skelton++)
    {
        for (int i = 0; i < 2; i++)
        {
            get_vertex(vertexes);
        }
    }
    solve(porygon_num, skelton_num, vertexes);
}