#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void solve() {
    int n;
    if (!(cin >> n)) return;
    
    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    // BUG: Initializing to 0 will fail if the array only has negative numbers!
    long long max_so_far = 0; 
    long long max_ending_here = 0;
    
    for (int i = 0; i < n; i++) {
        max_ending_here += a[i];
        if (max_ending_here < 0) {
            max_ending_here = 0;
        }
        max_so_far = max(max_so_far, max_ending_here);
    }
    cout << max_so_far << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (cin >> t) {
        while (t--) solve();
    }
    return 0;
}
