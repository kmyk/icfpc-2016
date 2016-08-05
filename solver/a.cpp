#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <set>
#include <map>
#include <queue>
#include <tuple>
#include <unordered_set>
#include <unordered_map>
#include <functional>
#include <cassert>
#include <boost/rational.hpp>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/segment.hpp>
#define repeat(i,n) for (int i = 0; (i) < (n); ++(i))
#define repeat_from(i,m,n) for (int i = (m); (i) < (n); ++(i))
#define repeat_reverse(i,n) for (int i = (n)-1; (i) >= 0; --(i))
#define repeat_from_reverse(i,m,n) for (int i = (n)-1; (i) >= (m); --(i))
#define whole(f,x,...) ([&](decltype((x)) y) { return (f)(begin(y), end(y), ## __VA_ARGS__); })(x)
typedef long long ll;
using namespace std;
template <class T> void setmax(T & a, T const & b) { if (a < b) a = b; }
template <class T> void setmin(T & a, T const & b) { if (b < a) a = b; }
template <typename T, typename X> auto vectors(T a, X x) { return vector<T>(x, a); }
template <typename T, typename X, typename Y, typename... Zs> auto vectors(T a, X x, Y y, Zs... zs) { auto cont = vectors(a, y, zs...); return vector<decltype(cont)>(x, cont); }

namespace mp = boost::multiprecision;
namespace bg = boost::geometry;
typedef boost::multiprecision::cpp_int integer;
typedef boost::rational<integer> rational;
typedef boost::geometry::model::d2::point_xy<rational, bg::cs::cartesian> point;
typedef boost::geometry::model::polygon<point> polygon;
typedef boost::geometry::model::segment<point> segment;

struct problem {
    vector<polygon> silhouette;
    vector<segment> skeleton;
};

struct solution {
    vector<point> source_points;
    vector<vector<point> > facets;
    vector<point> destination_points;
};

istream & operator >> (istream & in, point & a) {
    char ignore;
    rational x, y; in >> x >> ignore >> y;
    a = point(x, y);
    return in;
}

istream & operator >> (istream & in, problem & a) {
    a.silhouette.clear();
    int n; in >> n;
    while (-- n) {
        int m; in >> m;
        polygon p;
        while (-- m) {
            point q; in >> q;
            bg::append(p.outer(), q);
        }
        a.silhouette.push_back(p);
    }
    a.skeleton.clear();
    int k; in >> k;
    while (-- k) {
        point p, q;
        a.skeleton.push_back(segment(p, q));
    }
    return in;
}

ostream & operator << (ostream & out, point const & a) {
    return out << a.x() << ',' << a.y();
}

ostream & operator << (ostream & out, solution const & a) {
    assert (a.source_points.size() == a.destination_points.size());
    out << a.source_points.size() << endl;
    for (point p : a.source_points) {
        out << p << endl;
    }
    out << a.facets.size() << endl;
    for (auto && facet : a.facets) {
        out << facet.size();
        for (point p : facet) {
            out << ' ' << p;
        }
        out << endl;
    }
    for (point p : a.destination_points) {
        out << p << endl;
    }
    return out;
}

int main() {
    problem prob; cin >> prob;
    solution solt; cout << solt;
    return 0;
}
