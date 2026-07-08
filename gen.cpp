#include <iostream>
#include <vector>
#include <random>
#include <chrono>

using namespace std;

int main() {
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    
    // Exactly 1 test case per run
    int t = 1; 
    cout << t << "\n";
    
    while (t--) {
        int n = (rng() % 6) + 5; // Array size 5 to 10
        cout << n << "\n";
        
        for (int i = 0; i < n; i++) {
            // Generating numbers between -100 and 10 to guarantee mostly negative numbers
            int r = rng();
            int val = (r % 110) - 100;
            cout << val << (i == n - 1 ? "" : " ");
        }
        cout << "\n";
    }
    return 0;
}
