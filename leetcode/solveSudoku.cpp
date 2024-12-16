#include <iostream>
#include <vector>
#include <deque>
#include <stack>
#include <set>
#include <map>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include "ListNode.hpp"
using namespace std;

class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        stack<char> curr;
        vector<vector<bool>> visited(board.size(),vector<bool>(board[0].size(),false));
        for(int i=0;i<board.size();i++){
            for(int j=0;j<board[0].size();j++){
                if(checkExist(board,word,i,j,curr,visited)){
                    return true;
                }
            }
        }
        return false;
    }

    bool checkExist(vector<vector<char>>& board, string &word, int i, int j,stack<char> curr,vector<vector<bool>>& visited){
        int n = curr.size();
        if(n == word.size()){
            return true;
        }
        if(i<0 || i>=board.size() || j<0 || j>=board[0].size()){
            return false;
        }
        if(visited[i][j]){
            return false;
        }
        if(board[i][j] != word[n]){
            return false;
        }
        visited[i][j] = true;
        curr.push(board[i][j]);
        bool res = checkExist(board,word,i+1,j,curr,visited) || checkExist(board,word,i-1,j,curr,visited) || checkExist(board,word,i,j+1,curr,visited) || checkExist(board,word,i,j-1,curr,visited);
        visited[i][j] = false;
        curr.pop();
        return res;
    }
};

int main(){ 
    vector<vector<char>> board = {{'A','B','C','E'},{'S','F','C','S'},{'A','D','E','E'}};
    string word = "ABCCED";
    Solution s;
    cout<<s.exist(board, word)<<endl;
    return 0;
}