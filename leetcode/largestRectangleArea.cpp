#include <iostream>
#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        if(n == 0) return 0;
        int maxArea = 0;
        stack<int> st;
        st.push(0);
        for(int i = 1; i < n; i++) {
            while(!st.empty() && heights[st.top()] >= heights[i]) {
                int h = heights[st.top()];
                st.pop();
                int w = i;
                if(!st.empty()) w = i - st.top() - 1;
                maxArea = max(maxArea, h * w);
            }
            st.push(i);
        }
        while(!st.empty()) {
            int h = heights[st.top()];
            st.pop();
            int w = n;
            if(!st.empty()) w = n - st.top() - 1;
            maxArea = max(maxArea, h * w);
        }
        return maxArea;

        
    }
};

int main() {
    Solution s;
    vector<int> nums = {2,1,5,6,2,3};
    cout<<s.largestRectangleArea(nums);

    return 0;
}